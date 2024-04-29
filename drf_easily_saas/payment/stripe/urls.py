from django.urls import path, include
from . import views

app_name = 'payment'

# ---------------------------------- #
# VIEWS
# ---------------------------------- #
checkout_list_view = views.CheckoutView.as_view()


# ---------------------------------- #
# URLS
# ---------------------------------- #
checkout_urls = [
    path('session/', checkout_list_view, name='checkout'),

]

webhook_urls = [
    path('', views.WebhookView.as_view(), name='stripe-webhook'),
]


# ---------------------------------- #
# MAIN URLS
# ---------------------------------- #
urlpatterns = [
    path('checkout/', include(checkout_urls)),
    path('webhook/', include(webhook_urls)),
]