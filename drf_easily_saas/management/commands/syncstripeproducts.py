from django.core.management.base import BaseCommand
from drf_easily_saas.payment.stripe.sync.products import import_stripe_products

class Command(BaseCommand):
    help = 'Import products from Stripe'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting product import...'))
        try:
            import_stripe_products()
            self.stdout.write(self.style.SUCCESS('Successfully imported products from Stripe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing products: {e}'))
