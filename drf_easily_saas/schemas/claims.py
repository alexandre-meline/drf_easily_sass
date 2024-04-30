import stripe
from pydantic import BaseModel, field_validator, HttpUrl
from typing import List, Dict, Any, Union
from firebase_admin import auth

# Django
from django.contrib.auth.models import User


# From package
from drf_easily_saas.schemas.constants import STRIPE_SUBSCRIPTION_STATUS_TYPES
from drf_easily_saas.exceptions.base import ValidationError
from drf_easily_saas.exceptions.config import InvalidConfigurationError
# _Models
from drf_easily_saas.models import Subscription


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
    

class FirebaseClaimsPayment(ClaimsPayment):
    """
    This class is used to validate the claims.

    On this class, we validate the claims.

    Args:
    - status (str): Status of the user
    - customer_id (str): Customer ID
    - subscription_id (str): Subscription ID
    - plan_id (str): Plan ID
    - uid (str): User ID

    Returns:
    - status (str): Status of the user
    - customer_id (str): Customer ID
    - subscription_id (str): Subscription ID
    - plan_id (str): Plan ID
    """
    uid: str

    @field_validator('uid')
    def validate_uid(cls, v):
        if not v:
            raise ValidationError("UID cannot be empty")
        return v
    
    def update_state_token(cls, claims: ClaimsPayment, subscription: stripe.Subscription) -> Union[auth.UserRecord, None]:
        """
        Add custom claims to a Firebase user.
        """
        # Validate claims
        if not claims:
            return None
        # Add custom claims
        auth.set_custom_user_claims(cls.uid, claims.dict())
        # Check if claims are added
        if auth.get_user(cls.uid).custom_claims == claims.dict():
            print('Custom claims added to the user in firebase')
            # Ici on force la mise à jour du token pour que les nouvelles informations soient prises en compte
            # Ce qui à pour effet deconnecter le user de toutes ses sessions sur tous les devices
            # Il devra se reconnecter pour obtenir un nouveau token
            # Cela assure que les nouvelles informations sont prises en compte rapidement
            auth.revoke_refresh_tokens(cls.uid)

             # Get the user from the database with the uid
            user = User.objects.get(username=cls.uid)

            # Add or update the subscription to the database
            sub_table = Subscription.objects.update_or_create(
                user=user,
                provider='STRIPE',
                defaults={
                    'subscription_id': subscription.id,
                    'status': subscription.status,
                    'plan_id': subscription.plan.id,
                    'customer_id': subscription.customer,
                }
            )
            if sub_table:
                print(f'Subscription added to the database and custom claims added to the user')
                return sub_table
        return None