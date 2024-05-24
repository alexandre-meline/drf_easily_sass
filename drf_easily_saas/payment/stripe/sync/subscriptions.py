from datetime import datetime
from drf_easily_saas import settings
from drf_easily_saas.models import StripeSubscriptionModel, StripeCustomerModel
import stripe
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_CONFIG.secret_key

def import_stripe_subscriptions(limit: int = 100):
    try:
        subscriptions = stripe.Subscription.list(limit=limit)
        # print(subscriptions['data'])
        for sub in subscriptions.auto_paging_iter():
            customer_id = sub['customer']
            if customer_id:
                customer = StripeCustomerModel.objects.get(
                    id=customer_id
                )
                logger.error(f"Customer {customer_id} is found.")
                if not customer:
                    logger.error(f"Customer {customer_id} not found.")
                    continue
            StripeSubscriptionModel.objects.update_or_create(
                id=sub['id'],
                defaults={
                    'cancel_at_period_end': sub['cancel_at_period_end'],
                    'currency': sub['currency'],
                    'current_period_end': datetime.fromtimestamp(sub['current_period_end']),
                    'current_period_start': datetime.fromtimestamp(sub['current_period_start']),
                    'customer': customer,
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