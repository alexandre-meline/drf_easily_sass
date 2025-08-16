from django.contrib import admin
from .models import FirebaseUserInformations, SupabaseUserInformations
# Stripe
from .models import (
    StripeCustomerModel,
    StripeInvoiceModel,
    StripePlanModel,
    StripeProductModel,
    StripeSubscriptionModel,
    StripeSetupIntentModel
)

# Firebase
# ------------------------------------------------
admin.site.register(FirebaseUserInformations)

# Supabase
# ------------------------------------------------
admin.site.register(SupabaseUserInformations)

# Stripe
# ------------------------------------------------
admin.site.register(StripeCustomerModel)
admin.site.register(StripeInvoiceModel)
admin.site.register(StripePlanModel)
admin.site.register(StripeProductModel)
admin.site.register(StripeSubscriptionModel)
admin.site.register(StripeSetupIntentModel)