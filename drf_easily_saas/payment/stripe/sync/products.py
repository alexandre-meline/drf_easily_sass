from datetime import datetime
from drf_easily_saas import settings
from drf_easily_saas.models import StripeProductModel
import stripe

stripe.api_key = settings.STRIPE_CONFIG.secret_key

def import_stripe_products(limit: int = 100):
    try:
        products = stripe.Product.list(limit=limit)
        for prod in products['data']:
            StripeProductModel.objects.update_or_create(
                id=prod['id'],
                defaults={
                    'active': prod.get('active', True),
                    'default_price': prod.get('default_price'),
                    'description': prod.get('description'),
                    'metadata': prod.get('metadata', {}),
                    'name': prod.get('name'),
                    'object': prod.get('object'),
                    'created': datetime.fromtimestamp(prod.get('created')),
                    'images': prod.get('images', []),
                    'livemode': prod.get('livemode', False),
                    'marketing_features': prod.get('metadata', {}).get('marketing_features', []),
                    'package_dimensions': prod.get('package_dimensions'),
                    'shippable': prod.get('shippable'),
                    'statement_descriptor': prod.get('statement_descriptor'),
                    'tax_code': prod.get('tax_code'),
                    'unit_label': prod.get('unit_label'),
                    'updated': datetime.fromtimestamp(prod.get('updated')),
                    'url': prod.get('url'),
                }
            )
    except Exception as e:
        print(f"An error occurred: {e}")