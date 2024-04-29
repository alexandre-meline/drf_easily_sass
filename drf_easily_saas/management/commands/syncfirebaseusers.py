from django.core.management.base import BaseCommand
from firebase_admin import auth
from django.contrib.auth.models import User
from drf_easily_saas.models import FirebaseUserInformations

class Command(BaseCommand):
    """
    Command to synchronise users from Firebase
    
    Usage:
        python3 manage.py syncfirebaseusers
    """
    help = 'Users synchronisation from Firebase'

    def handle(self, *args, **options):
        header_message = """
########################################################
#                                                      #
#           Firebase User Synchronisation              #
#                                                      #
########################################################
        """
        separator = "-" * 50
        self.stdout.write(self.style.SUCCESS(header_message))
        firebase_users = auth.list_users().iterate_all()

        for firebase_user in firebase_users:
            if not firebase_user.email:
                user, created = User.objects.get_or_create(username=firebase_user.uid)
            else:
                user, created = User.objects.get_or_create(username=firebase_user.uid, email=firebase_user.email)

            if created:
                user.set_unusable_password()
                user.save()

                FirebaseUserInformations.objects.create(
                    user=user,
                    email_verified=firebase_user.email_verified,
                    sign_in_provider=firebase_user.provider_id
                )
                self.stdout.write(self.style.SUCCESS(f'User sync > ID: {user.username} > Email: {user.email}'))
        self.stdout.write(self.style.SUCCESS('Users synchronisation completed'))

        user_count = User.objects.count()

        self.stdout.write(self.style.SUCCESS(separator))
        self.stdout.write(self.style.SUCCESS(f'Users count: {user_count}'))