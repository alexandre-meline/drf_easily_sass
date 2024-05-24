import stripe
import logging
from drf_easily_saas import settings
from drf_easily_saas.models import StripePlanModel, StripeProductModel
from datetime import datetime

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_CONFIG.secret_key

def import_stripe_plans(limit: int = 100):
    try:
        plans = stripe.Plan.list(limit=limit)
        logger.info(f"Importing {len(plans)} plans from Stripe")
        for stripe_plan in plans.auto_paging_iter():
            product_id = stripe_plan['product']
            if product_id:
                product = StripeProductModel.objects.get(
                    id=product_id
                )
                logger.error(f"Product {product_id} is found.")
                if not product:
                    logger.error(f"Product {product_id} not found.")
                    continue

            StripePlanModel.objects.update_or_create(
                id=stripe_plan['id'],
                defaults={
                    'active': stripe_plan['active'],
                    'amount': stripe_plan.get('amount'),
                    'amount_decimal': stripe_plan.get('amount_decimal'),
                    'currency': stripe_plan['currency'],
                    'interval': stripe_plan['interval'],
                    'interval_count': stripe_plan['interval_count'],
                    'billing_scheme': stripe_plan['billing_scheme'],
                    'created': datetime.fromtimestamp(stripe_plan['created']),
                    'livemode': stripe_plan['livemode'],
                    'metadata': stripe_plan.get('metadata', {}),
                    'nickname': stripe_plan.get('nickname'),
                    'product': product,
                    'tiers_mode': stripe_plan.get('tiers_mode'),
                    'transform_usage': stripe_plan.get('transform_usage'),
                    'trial_period_days': stripe_plan.get('trial_period_days'),
                    'usage_type': stripe_plan['usage_type'],
                }
            )
            logger.info(f"Plan {stripe_plan['id']} imported successfully.")
        print("Plans imported successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

