from datetime import datetime
from drf_easily_saas import settings
from drf_easily_saas.models import StripeSubscriptionModel
import stripe

stripe.api_key = settings.STRIPE_CONFIG.secret_key

def import_stripe_subscriptions(limit: int = 100):
    try:
        subscriptions = stripe.Subscription.list(limit=limit)
        # print(subscriptions['data'])
        for sub in subscriptions.auto_paging_iter():
            StripeSubscriptionModel.objects.update_or_create(
                id=sub['id'],
                defaults={
                    'cancel_at_period_end': sub['cancel_at_period_end'],
                    'currency': sub['currency'],
                    'current_period_end': datetime.fromtimestamp(sub['current_period_end']),
                    'current_period_start': datetime.fromtimestamp(sub['current_period_start']),
                    'customer': sub['customer'],
                    'default_payment_method': sub['default_payment_method'],
                    'description': sub.get('description'),
                    'items': sub['items'],
                    'latest_invoice': sub.get('latest_invoice'),
                    'metadata': sub.get('metadata', {}),
                    'pending_setup_intent': sub.get('pending_setup_intent'),
                    'pending_update': sub.get('pending_update'),
                    'status': sub['status'],
                }
            )
    except Exception as e:
        print(f"An error occurred: {e}")