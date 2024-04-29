from firebase_admin import auth
from typing import List, Union

# Django
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings as dj_settings
from django.contrib.auth.models import User

# From package
from drf_easily_saas.models import FirebaseUserInformations
from drf_easily_saas.schemas.claims import ClaimsPayment

# ---------------------------------------- AUTHENTICATION ---------------------------------------- #
class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        # Get token from any scheme (Bearer, JWT, etc.)
        token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(token, check_revoked=True)

            # Extract user data
            uid = decoded_token['uid']
            email = decoded_token['email']
            email_verified = decoded_token['email_verified']
            provider = decoded_token['firebase']['sign_in_provider']

        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed({'error': 'Invalid authentication token.'})
        except auth.ExpiredIdTokenError:
            raise exceptions.AuthenticationFailed({'error': 'Expired authentication token.'})
        except auth.RevokedIdTokenError:
            raise exceptions.AuthenticationFailed({'error': 'Revoked authentication token.'})
        except Exception as e:
            raise exceptions.AuthenticationFailed({'error': 'Could not authenticate.'})

        user, created = User.objects.get_or_create(username=uid, email=email)
        if created:
            # Disable user password
            user.set_unusable_password()
            user.save()

            # Firebase user informations (aud, email_verified, sign_in_provider)
            firebase_user = FirebaseUserInformations.objects.create(
                user=user,
                email_verified=email_verified,
                sign_in_provider=provider
            )
        return user or None, firebase_user or None

# ---------------------------------------- FIREBASE UTILS ---------------------------------------- #

def import_users() -> List[User]:
    """
    Import users from Firebase and sync with Django's User model.
    """
    new_users = False
    deleted_users = False 

    firebase_users = auth.list_users().iterate_all()
    django_users = User.objects.all()

    print("#"*100)
    print("Firebase syncing users...")
    for firebase_user in firebase_users:
        if not firebase_user.email:
            user, created = User.objects.get_or_create(username=firebase_user.uid)
        else:
            user, created = User.objects.get_or_create(username=firebase_user.uid, email=firebase_user.email)

        if created:
            new_users = True
            user.set_unusable_password()
            
            user.save()

            FirebaseUserInformations.objects.create(
                user=user,
                email_verified=firebase_user.email_verified,
                sign_in_provider=firebase_user.provider_id
            )
            # Message for each user
            print(f'User sync > ID: {user.username} > Email: {user.email} > Created: {created}')

    # Delete users that are not in Firebase
    for django_user in django_users:
        try:
            auth.get_user(django_user.username)
        except auth.UserNotFoundError:
            deleted_users = True    
            django_user.delete()
            print(f'User sync > ID: {django_user.username} > Deleted: True')

    nbr_firebase_users = len([user for user in auth.list_users().iterate_all()])
    nbr_django_users = len([user for user in User.objects.all()])

    if nbr_django_users == nbr_firebase_users:
        print("User sync > Synced successfully")
        print(f'User sync > Total Django users: {nbr_django_users} > Total Firebase users: {nbr_firebase_users}')
    else:
        print("User sync > Sync failed")
        print(f'User sync > Total Django users: {nbr_django_users} > Total Firebase users: {nbr_firebase_users}')
    
    print("#"*100)
    print()
    return new_users, deleted_users
    
