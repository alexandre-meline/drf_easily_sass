from django.conf import settings as dj_setting
from drf_easily_saas.schemas.utils import validate_settings

# -------------------------------------------- #
# Settings
# -------------------------------------------- #
EASILY_CONFIG = validate_settings(dj_setting.EASILY)
FRONTEND_URL = EASILY_CONFIG.frontend_url

# -------------------------------------------- #
# Authentication
# -------------------------------------------- #
AUTH_PROVIDER = EASILY_CONFIG.auth_provider
# _ Firebase
FIREBASE_CONFIG = EASILY_CONFIG.firebase_config


# -------------------------------------------- #
# Payments
# -------------------------------------------- #
PAYMENT_PROVIDER = EASILY_CONFIG.payment_provider
# Stripe
STRIPE_CONFIG = EASILY_CONFIG.stripe_config
STRIPE_SUBSCRIPTION_CONFIG = STRIPE_CONFIG.subscription
