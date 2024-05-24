from django.core.management.base import BaseCommand
from drf_easily_saas.payment.stripe.sync.subscriptions import import_stripe_subscriptions

class Command(BaseCommand):
    help = 'Import products from Stripe'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting subscription import...'))
        try:
            import_stripe_subscriptions()
            self.stdout.write(self.style.SUCCESS('Successfully imported subscriptions from Stripe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing subscriptions: {e}'))