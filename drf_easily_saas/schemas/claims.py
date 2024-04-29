from pydantic import BaseModel, field_validator, HttpUrl
from typing import List, Dict, Any, Union

# From package
from drf_easily_saas.schemas.constants import STRIPE_SUBSCRIPTION_STATUS_TYPES
from drf_easily_saas.exceptions.base import ValidationError
from drf_easily_saas.exceptions.config import InvalidConfigurationError


class ClaimsPayment(BaseModel):
    """
    This class is used to validate the claims.

    On this class, we validate the claims.

    Args:
    - status (str): Status of the user
    - customer_id (str): Customer ID
    - subscription_id (str): Subscription ID
    - plan_id (str): Plan ID

    Returns:
    - status (str): Status of the user
    - customer_id (str): Customer ID
    - subscription_id (str): Subscription ID
    - plan_id (str): Plan ID
    """
    status: str
    customer_id: str
    subscription_id: str
    plan_id: str

    @field_validator('status')
    def validate_status(cls, v):
        if v not in STRIPE_SUBSCRIPTION_STATUS_TYPES:
            raise ValidationError("Status must be either active, suspend, trialing, past_due, unpaid, or canceled")
        return v

    @field_validator('customer_id')
    def validate_customer_id(cls, v):
        if not v:
            raise ValidationError("Customer ID cannot be empty")
        return v

    @field_validator('subscription_id')
    def validate_subscription_id(cls, v):
        if not v:
            raise ValidationError("Subscription ID cannot be empty")
        return v

    @field_validator('plan_id')
    def validate_plan_id(cls, v):
        if not v:
            raise ValidationError("Plan ID cannot be empty")
        return v