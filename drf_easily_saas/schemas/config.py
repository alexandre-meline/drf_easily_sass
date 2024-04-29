from pydantic import BaseModel, field_validator, HttpUrl
from typing import List, Dict, Any, Union

from django.conf import settings as django_settings

# Drf Easily Saas
from drf_easily_saas.utils.urls import remove_last_slash
# Child schemas
from drf_easily_saas.schemas.constants import (
    PAYMENT_VALID_PROVIDER, 
    AUTH_VALID_PROVIDER,
    )
from drf_easily_saas.schemas.stripe import StripeConfig
from drf_easily_saas.schemas.firebase import FirebaseConfig
# Exceptions
from drf_easily_saas.exceptions.config import InvalidConfigurationError

# -------------------------------------------- #
# Pydantic settings schema validation
# -------------------------------------------- #

# Main settings schema
class EasilyConfig(BaseModel):
    auth_provider: str
    payment_provider: str
    frontend_url: HttpUrl
    firebase_config: FirebaseConfig = None
    stripe_config: StripeConfig = None
    
    @field_validator('auth_provider')
    def validate_auth_provider(cls, v):
        valid_providers = AUTH_VALID_PROVIDER
        if v not in valid_providers:
            raise InvalidConfigurationError('Authentification provider is not valid')
        if v == "firebase":
            # Check if config is provided
            if "firebase_config" not in django_settings.EASILY:
                raise InvalidConfigurationError("Firebase config is required")
        return v
     
    @field_validator('payment_provider')
    def validate_payment_provider(cls, v):
        valid_providers = PAYMENT_VALID_PROVIDER
        if v not in valid_providers:
            raise InvalidConfigurationError('Payment provider is not valid')
        
        if v == "stripe":
            # Check if config is provided
            if "stripe_config" not in django_settings.EASILY:
                raise InvalidConfigurationError("Stripe config is required")
        return v
    
    # Converti le frontend_url en str
    @field_validator('frontend_url')
    def validate_frontend_url(cls, v):
        return remove_last_slash(str(v))

# -------------------------------------------- #