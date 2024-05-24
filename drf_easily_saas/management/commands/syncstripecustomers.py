from django.core.management.base import BaseCommand
from drf_easily_saas.payment.stripe.sync.customers import import_stripe_customers

class Command(BaseCommand):
    help = 'Import products from Stripe'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting customer import...'))
        try:
            import_stripe_customers()
            self.stdout.write(self.style.SUCCESS('Successfully imported customers from Stripe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing customers: {e}'))