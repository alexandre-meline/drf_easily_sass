from django.core.management.base import BaseCommand
from supabase import create_client, Client
from django.contrib.auth.models import User
from drf_easily_saas.models import SupabaseUserInformations
from django.conf import settings as dj_settings

class Command(BaseCommand):
    """
    Command to synchronise users from Supabase
    
    Usage:
        python3 manage.py syncsupabaseusers
    """
    help = 'Users synchronisation from Supabase'

    def handle(self, *args, **options):
        header_message = """
########################################################
#                                                      #
#           Supabase User Synchronisation              #
#                                                      #
########################################################
        """
        separator = "-" * 50
        self.stdout.write(self.style.SUCCESS(header_message))
        
        try:
            # Get supabase config from Django settings
            supabase_config = dj_settings.EASILY.get('supabase_config', {})
            url = supabase_config.get('url')
            service_role_key = supabase_config.get('service_role_key')
            
            if not url or not service_role_key:
                self.stdout.write(self.style.ERROR('Supabase configuration not found or incomplete'))
                return
            
            # Create supabase client with service role key for admin operations
            supabase: Client = create_client(url, service_role_key)

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
                    user.set_unusable_password()
                    user.save()

                    SupabaseUserInformations.objects.create(
                        user=user,
                        email_verified=email_verified,
                        sign_in_provider=provider
                    )
                    self.stdout.write(self.style.SUCCESS(f'User sync > ID: {user.username} > Email: {user.email}'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error syncing users from Supabase: {str(e)}'))
            return
            
        self.stdout.write(self.style.SUCCESS('Users synchronisation completed'))

        user_count = User.objects.count()

        self.stdout.write(self.style.SUCCESS(separator))
        self.stdout.write(self.style.SUCCESS(f'Users count: {user_count}'))