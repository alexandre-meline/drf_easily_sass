from django.core.management.base import BaseCommand
from drf_easily_saas.payment.stripe.sync.plans import import_stripe_plans

class Command(BaseCommand):
    help = 'Import all Stripe plans into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting plan import...'))
        try:
            import_stripe_plans()
            self.stdout.write(self.style.SUCCESS('Successfully imported plans from Stripe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing plans: {e}'))
