# --------------------------------------------- #
# Auth provider configuration
# --------------------------------------------- #
AUTH_VALID_PROVIDER=['firebase', 'keycloak', 'cognito', 'auth0']


# --------------------------------------------- #
# Payment provider configuration
# --------------------------------------------- #
PAYMENT_VALID_PROVIDER=['stripe', 'lemonsqueezy']
# _ Stripe
STRIPE_VERIF_STRATEGY = ['secret', 'apikey']
STRIPE_PAYMENT_METHODS_ALLOWED = ['card', 'paypal']
STRIPE_SUBSCRIPTION_STATUS_TYPES=['incomplete', 'incomplete_expired', 'trialing', 'active', 'past_due', 'canceled', 'unpaid', 'paused']