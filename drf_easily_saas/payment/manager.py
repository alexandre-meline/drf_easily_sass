import stripe
import json
from typing import Union, List, Dict, Any
# Drf Easily Saas
from drf_easily_saas.settings import AUTH_PROVIDER, PAYMENT_PROVIDER, STRIPE_CONFIG, STRIPE_SUBSCRIPTION_CONFIG, FRONTEND_URL

# Drf Easily Saas exceptions
from drf_easily_saas.exceptions.stripe import StripePaymentProcessingError
from drf_easily_saas.schemas.stripe import StripeBaseSubscription
from drf_easily_saas.schemas.claims import FirebaseClaimsPayment

# User methods and classes
from drf_easily_saas.models import User, Subscription


# Ici je vais créer une classe qui va gérer les paiements avec Stripe et LemonSqueezy, 
# aussi elle gérera la synchronisation des utilisateurs avec le provider d'authentification défini dans les settings.
class PaymentManager:
    def __init__(self):
        self.payment_provider = PAYMENT_PROVIDER
        self.auth_provider = AUTH_PROVIDER


class StripeManager(PaymentManager):
    def __init__(self):
        self.config = STRIPE_CONFIG
        self.frontend_url = FRONTEND_URL
        self.webhook_verif_strategy = self.config.webhook_verif_strategy
        self.endpoint_secret = self.config.endpoint_secret
        self.public_key = self.config.public_key

        # Initialize Stripe
        stripe.api_key = self.config.secret_key
        super().__init__()


    # -------------------------------------------- #
    # Checkout session
    # -------------------------------------------- #
    def create_checkout_session(self, subscription_schema: dict) -> stripe.checkout.Session:
        """
        Create a checkout session with Stripe.
        """
        try:
            # Validate the subscription schema for Stripe from define in settings.py in project
            subscription_schema_valid = StripeBaseSubscription(**subscription_schema)
            # Add user informations to metadata if not already present
            session = stripe.checkout.Session.create(**subscription_schema_valid.to_dict())
        except stripe.error.StripeError as e:
            raise StripePaymentProcessingError(str(e))
        return session
        
    # -------------------------------------------- #
    # Webhooks
    # -------------------------------------------- #
    def verify_webhook(self, payload, sig_header = None):
        """
        Verify webhook from Stripe.
        """
        if self.webhook_verif_strategy == "apikey":
            return self.verify_webhook_apikey(payload)
        elif self.webhook_verif_strategy == "endpoint_secret":
            return self.verify_webhook_endpoint_secret(payload, sig_header)
        else:
            raise Exception("Webhook verification strategy not found")    

    def verify_webhook_apikey(self, payload):
        """
        Verify webhook from Stripe with api key.
        """
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            # Invalid payload
            return None
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return None
        return event

    def verify_webhook_endpoint_secret(self, payload: str, sig_header: str):
        """
        Verify webhook from Stripe with endpoint secret.
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.config.endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return None
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return None
        return event
    
    # Webhooks handler
    # ---------------- #
    def handle_stripe_event(self, event: dict):
        event_type = self._normalize_event_type(event['type'])
        event_data = event['data']['object']

        handler = getattr(self, f"handle_{event_type}", None)
        
        if handler is None:
            raise Exception(f"Webhook handler for {event_type} not found")

        return handler(event_data)

    # Handle the event Checkouts
    # -------------------------------------------- #
    def handle_checkout_session_async_payment_failed(self, session):
        print('Payment failed')
        # Traitez l'échec du paiement ici
        return True

    def handle_checkout_session_async_payment_succeeded(self, session):
        print('Payment succeeded')
        # Traitez la réussite du paiement ici
        return True

    def handle_checkout_session_completed(self, event_data) -> Union[Subscription, None]:
        session_ = event_data
        # Mets à jour le profile de l'utilisateur dans Firebase
        uid = session_['metadata']['uid']
        subscription_id = session_['subscription']

        # [Stripe] Add uid in customer metadata
        customer = self._add_customer_metadata(session_['customer'], {'uid': uid})

        # [Stripe] ajoute les metadata à l'abonnement de l'utilisateur dans Stripe
        # Ajoute: uid
        subscription = self._add_subscribtion_meta(subscription_id, {'uid': uid})

        # [Firebase] Ajoute les custom claims au user dans Firebase
        # Cela aura pour effet de mettre à jour le token de l'utilisateur et de le deconnecter de toutes ses sessions
        custom_claims = FirebaseClaimsPayment(
            status=subscription.status,
            customer_id=customer.id,
            subscription_id=subscription_id,
            plan_id=subscription.plan.id,
            uid=uid
        )

        if custom_claims.update_state_token(custom_claims, subscription):
            return subscription
        else:
            print('Error adding subscription to the database')
            return None

    def handle_checkout_session_expired(self, session):
        print('Payment expired')
        # Traitez l'expiration du paiement ici
        return None

    # -------------------------------------------- #
    # Handle the event Subscriptions
    # -------------------------------------------- #
    def handle_customer_subscription_created(self, subscription):
        print('Subscription created')
        # Traitez la création de l'abonnement ici
        return True

    def handle_customer_subscription_updated(self, subscription):
        print('Subscription updated')
        # Traitez la mise à jour de l'abonnement ici
        return True

    def handle_customer_subscription_deleted(self, event_data):
        print('Subscription deleted')
        subscription = event_data

        # Mets à jour le profile de l'utilisateur dans Firebase
        uid = subscription['metadata']['uid']
        subscription_id = subscription['id']
        
        # [Firebase] Ajoute les custom claims au user dans Firebase
        # Cela aura pour effet de mettre à jour le token de l'utilisateur et de le deconnecter de toutes ses sessions
        custom_claims = FirebaseClaimsPayment(
            status=subscription.status,
            customer_id=subscription.customer,
            subscription_id=subscription_id,
            plan_id=subscription.plan.id,
            uid=uid
        )

        if custom_claims.update_state_token(custom_claims, subscription):
            return subscription
        else:
            print('Error adding subscription to the state')
            return None

    # -------------------------------------------- #
    # Private methods
    # -------------------------------------------- #
    # _ Subscription methods
    def _add_subscribtion_meta(self, subscription_id: int , metadata: dict) -> Union[stripe.Subscription, None]:
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription.metadata = metadata
        subscription.save()
        if subscription.metadata == metadata:
            return subscription
        return None
    
    def _get_subscribtion_meta(self, subscription_id: int) -> Union[stripe.Subscription, None]:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription.metadata
    
    # _ Customer methods
    def _add_customer_metadata(self, customer_id: int, metadata: dict) -> Union[stripe.Customer, None]:
        customer = stripe.Customer.retrieve(customer_id)
        customer.metadata = metadata
        customer.save()
        if customer.metadata == metadata:
            return customer
        return None
    
    def _get_customer_metadata(self, customer_id: int) -> Union[stripe.Customer, None]:
        customer = stripe.Customer.retrieve(customer_id)
        return customer.metadata

    # _ Utils
    def _normalize_event_type(self, event_type: str) -> str:
        return event_type.replace('.', '_')