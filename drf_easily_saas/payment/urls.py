from django.urls import path, include
from drf_easily_saas.settings import PAYMENT_PROVIDER

app_name = 'payment'

stripe_routes = [
    path('stripe/', include('drf_easily_saas.payment.stripe.urls')),
]

urlpatterns = []

if PAYMENT_PROVIDER == 'stripe':
    urlpatterns += stripe_routes
