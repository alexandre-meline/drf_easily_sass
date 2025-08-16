from supabase import create_client, Client
import jwt
from typing import List, Union

# Django
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings as dj_settings
from django.contrib.auth.models import User

# From package
from drf_easily_saas.models import SupabaseUserInformations
from drf_easily_saas.schemas.claims import ClaimsPayment

# ---------------------------------------- AUTHENTICATION ---------------------------------------- #
class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        # Get token from any scheme (Bearer, JWT, etc.)
        token = auth_header.split(' ').pop()
        try:
            # Get supabase config from Django settings
            supabase_config = dj_settings.EASILY.get('supabase_config', {})
            url = supabase_config.get('url')
            anon_key = supabase_config.get('anon_key')
            
            if not url or not anon_key:
                raise exceptions.AuthenticationFailed({'error': 'Supabase configuration not found.'})
            
            # Create supabase client
            supabase: Client = create_client(url, anon_key)
            
            # Verify the JWT token
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            # Extract user data from JWT
            uid = decoded_token.get('sub')
            email = decoded_token.get('email', '')
            email_verified = decoded_token.get('email_confirmed', False)
            provider = decoded_token.get('app_metadata', {}).get('provider', 'email')

            if not uid:
                raise exceptions.AuthenticationFailed({'error': 'Invalid token: missing user ID.'})

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({'error': 'Invalid authentication token.'})
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({'error': 'Expired authentication token.'})
        except Exception as e:
            raise exceptions.AuthenticationFailed({'error': 'Could not authenticate.'})

        user, created = User.objects.get_or_create(username=uid, email=email)
        if created:
            # Disable user password
            user.set_unusable_password()
            user.save()

            # Supabase user informations (email_verified, sign_in_provider)
            supabase_user = SupabaseUserInformations.objects.create(
                user=user,
                email_verified=email_verified,
                sign_in_provider=provider
            )
        return user, None

# ---------------------------------------- SUPABASE UTILS ---------------------------------------- #

def import_users() -> List[User]:
    """
    Import users from Supabase and sync with Django's User model.
    """
    new_users = False
    deleted_users = False

    # Get supabase config from Django settings
    supabase_config = dj_settings.EASILY.get('supabase_config', {})
    url = supabase_config.get('url')
    service_role_key = supabase_config.get('service_role_key')
    
    if not url or not service_role_key:
        raise Exception("Supabase configuration not found or incomplete")
    
    # Create supabase client with service role key for admin operations
    supabase: Client = create_client(url, service_role_key)

    django_users = User.objects.all()

    print("#"*100)
    print("Supabase syncing users...")
    
    try:
        # Get all users from Supabase Auth
        response = supabase.auth.admin.list_users()
        supabase_users = response.users if hasattr(response, 'users') else []
        
        for supabase_user in supabase_users:
            uid = supabase_user.id
            email = supabase_user.email or ''
            email_verified = supabase_user.email_confirmed or False
            provider = supabase_user.app_metadata.get('provider', 'email') if supabase_user.app_metadata else 'email'
            
            if not email:
                user, created = User.objects.get_or_create(username=uid)
            else:
                user, created = User.objects.get_or_create(username=uid, email=email)

            if created:
                new_users = True
                user.set_unusable_password()
                user.save()

                SupabaseUserInformations.objects.create(
                    user=user,
                    email_verified=email_verified,
                    sign_in_provider=provider
                )
                # Message for each user
                print(f'User sync > ID: {user.username} > Email: {user.email} > Created: {created}')

        # Delete users that are not in Supabase
        supabase_uids = [user.id for user in supabase_users]
        for django_user in django_users:
            if django_user.username not in supabase_uids:
                # Check if this user has Supabase information (to avoid deleting Firebase users)
                if SupabaseUserInformations.objects.filter(user=django_user).exists():
                    deleted_users = True    
                    django_user.delete()
                    print(f'User sync > ID: {django_user.username} > Deleted: True')

        nbr_supabase_users = len(supabase_users)
        nbr_django_users = len([user for user in User.objects.all()])

        if nbr_django_users >= nbr_supabase_users:
            print("User sync > Synced successfully")
            print(f'User sync > Total Django users: {nbr_django_users} > Total Supabase users: {nbr_supabase_users}')
        else:
            print("User sync > Sync failed")
            print(f'User sync > Total Django users: {nbr_django_users} > Total Supabase users: {nbr_supabase_users}')
            
    except Exception as e:
        print(f"Error syncing users from Supabase: {str(e)}")
    
    print("#"*100)
    print()
    return new_users, deleted_users