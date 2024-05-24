from datetime import datetime
from drf_easily_saas import settings
from drf_easily_saas.models import StripeCustomerModel
import stripe

stripe.api_key = settings.STRIPE_CONFIG.secret_key

def import_stripe_customers(limit: int = 100):
    try:
        customers = stripe.Customer.list(limit=limit)
        for cust in customers['data']:
            StripeCustomerModel.objects.update_or_create(
                id=cust['id'],
                defaults={
                    'address': cust.get('address'),
                    'description': cust.get('description'),
                    'email': cust.get('email'),
                    'metadata': cust.get('metadata', {}),
                    'name': cust.get('name'),
                    'phone': cust.get('phone'),
                    'shipping': cust.get('shipping'),
                }
            )
    except Exception as e:
        print(f"An error occurred: {e}")