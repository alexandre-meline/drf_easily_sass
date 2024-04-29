from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

# Drf Easily Saas
from drf_easily_saas.exceptions.stripe import InvalidStripeConfigurationError
from drf_easily_saas.schemas.constants import STRIPE_VERIF_STRATEGY, STRIPE_PAYMENT_METHODS_ALLOWED


# -------------------------------------------- #
# Stripe settings schema validation
# -------------------------------------------- #
"""
Base model subscribtion config
client_reference_id=uid,
customer_email=uemail,
payment_method_types=payment_methods,
line_items=[
    {
        'price': price_id,
        'quantity': quantity,
    },
],
mode=mode,
success_url=concat_urls(FRONTEND_URL, success_url),
cancel_url=concat_urls(FRONTEND_URL, cancel_url),
metadata=metadata
billing_address_collection='auto',
shipping_address_collection={
    'allowed_countries': ['US', 'CA', 'FR'],
},
automatic_tax={'enabled': True},
"""
class StripeBaseSubscription(BaseModel):
    client_reference_id: str = None
    customer_email: str = None
    payment_method_types: List[str] = ['card']
    line_items: List[Dict[str, Union[str, Union[str, int]]]] = None
    mode: str = "subscription"
    success_url: str = "/success"
    cancel_url: str = "/cancel"
    metadata: Dict[str, Any] = None
    # Addons for subscription
    billing_address_collection: str = None
    shipping_address_collection: Dict[str, Union[str, List[str]]] = None
    automatic_tax: Dict[str, bool] = None
    
    @field_validator('client_reference_id')
    def validate_client_reference_id(cls, v):
        return v
    
    @field_validator('customer_email')
    def validate_customer_email(cls, v):
        return v
    
    @field_validator('payment_method_types')
    def validate_payment_method_types(cls, v):
        for method in v:
            if method not in STRIPE_PAYMENT_METHODS_ALLOWED:
                raise InvalidStripeConfigurationError(f'Stripe payment method {method} is not valid use {STRIPE_PAYMENT_METHODS_ALLOWED} instead')
        return v
    
    @field_validator('line_items')
    def validate_line_items(cls, v):
        for item in v:
            if 'price' not in item:
                raise InvalidStripeConfigurationError(f'Stripe line item must have price key')
            if 'quantity' not in item:
                raise InvalidStripeConfigurationError(f'Stripe line item must have quantity key')
        return v
    
    @field_validator('mode')
    def validate_mode(cls, v):
        if v not in ['payment', 'subscription']:
            raise InvalidStripeConfigurationError(f'Stripe mode {v} is not valid use payment or subscription instead')
        return v
    
    @field_validator('success_url')
    def validate_success_url(cls, v):
        return v
    
    @field_validator('cancel_url')
    def validate_cancel_url(cls, v):
        return v
    
    @field_validator('metadata')
    def validate_metadata(cls, v):
        return v

    @field_validator('billing_address_collection')
    def validate_billing_address_collection(cls, v):
        if v is None:
            return v
        if v not in ['auto', 'required', 'off']:
            raise InvalidStripeConfigurationError(f'Stripe billing address collection {v} is not valid use auto, required or off instead')
        return v
    
    @field_validator('shipping_address_collection')
    def validate_shipping_address_collection(cls, v):
        if not isinstance(v, dict):
            raise InvalidStripeConfigurationError(f'Stripe shipping address collection must be a dict')
        if 'allowed_countries' not in v:
            raise InvalidStripeConfigurationError(f'Stripe shipping address collection must have allowed_countries key')
        if not isinstance(v['allowed_countries'], list):
            raise InvalidStripeConfigurationError(f'Stripe shipping address collection allowed_countries must be a list')
        return v
    
    @field_validator('automatic_tax')
    def validate_automatic_tax(cls, v):
        if not isinstance(v, dict):
            raise InvalidStripeConfigurationError(f'Stripe automatic tax must be a dict')
        if 'enabled' not in v:
            raise InvalidStripeConfigurationError(f'Stripe automatic tax must have enabled key')
        if not isinstance(v['enabled'], bool):
            raise InvalidStripeConfigurationError(f'Stripe automatic tax enabled must be a boolean')
        return v
    
    # Deserialization method
    def to_dict(self):
        sub = self.dict()
        # Si les paramètres billing_address_collection, shipping_address_collection, automatic_tax sont None, on les enlève
        if self.billing_address_collection is None:
            sub.pop('billing_address_collection')
        if self.shipping_address_collection is None:
            sub.pop('shipping_address_collection')
        if self.automatic_tax is None:
            sub.pop('automatic_tax')
        return sub
    

class StripeConfig(BaseModel):
    public_key: str
    secret_key: str
    webhook_verif_strategy: str = "apikey"
    endpoint_secret: str = None
    subscription: StripeBaseSubscription = None

    @field_validator('public_key')
    def validate_public_key(cls, v):
        return v
    
    @field_validator('secret_key')
    def validate_secret_key(cls, v):
        return v
    
    @field_validator('endpoint_secret')
    def validate_endpoint_secret(cls, v):
        return v
    
    @field_validator('webhook_verif_strategy')
    def validate_webhook_verif_strategy(cls, v):
        if v not in STRIPE_VERIF_STRATEGY:
            raise InvalidStripeConfigurationError(f'Stripe webhook verification strategy is not valid use {STRIPE_VERIF_STRATEGY} instead')
        return v

    @field_validator('subscription')
    def validate_subscription(cls, v):
        return v