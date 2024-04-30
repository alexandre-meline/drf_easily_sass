import stripe

# Django
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# From package
from drf_easily_saas.utils.urls import concat_urls
from drf_easily_saas.settings import EASILY_CONFIG, STRIPE_CONFIG, STRIPE_SUBSCRIPTION_CONFIG
from drf_easily_saas.payment.serializers import SubscriptionSerializer
from drf_easily_saas.payment.stripe.serializers import CheckoutSerializer, CheckoutSessionSerializer
from drf_easily_saas.exceptions.stripe import StripePaymentProcessingError
from drf_easily_saas.payment.manager import StripeManager


# -------------------------------------------- #
stripe.api_key = STRIPE_CONFIG.secret_key
frontend_url = EASILY_CONFIG.frontend_url

# -------------------------------------------- #

# -------------------------------------------- #
# Checkout
# -------------------------------------------- #
class CheckoutView(APIView):
    serializer_class = CheckoutSerializer
    stripe_manager = StripeManager()

    @extend_schema(
        request=CheckoutSerializer,
        responses=CheckoutSessionSerializer
    )
    def post(self, request):
        try:
            checkout_datas = self.validate_request_data(request.data)
            checkout_session = self.stripe_manager.create_checkout_session(checkout_datas)
            return Response(CheckoutSessionSerializer(checkout_session).data, status=status.HTTP_201_CREATED)
        except StripePaymentProcessingError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def validate_request_data(self, data):
        # Ajoutez des validations ici
        # ...
        price_id = data.get('price_id')
        uid = data.get('uid')
        user_email = data.get('user_email')
        success_url = data.get('success_url')
        cancel_url = data.get('cancel_url')
        metadata = data.get('metadata') if 'metadata' in data else {}

        checkout_params = {
            'client_reference_id': uid,
            'customer_email': user_email,
            'payment_method_types': ['card', 'paypal'],
            'line_items': [
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            'mode': 'subscription',
            'success_url': concat_urls(frontend_url, success_url),
            'cancel_url': concat_urls(frontend_url, cancel_url),
            'metadata': {
                'uid': uid,
                'user_email': user_email,
            }
        }

        return checkout_params


# -------------------------------------------- #
# Webhook
# -------------------------------------------- #
    
class WebhookView(APIView):
    permission_classes = []
    
    def post(self, request):
        stripe_manager = StripeManager()
        payload = request.body

        # Verify the event by using the endpoint secret
        event_is_valid = stripe_manager.verify_webhook(payload)

        if event_is_valid:
            event = stripe_manager.handle_stripe_event(event_is_valid)
            return Response(event, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)