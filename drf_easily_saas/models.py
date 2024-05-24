from django.db import models
from django.contrib.auth.models import User

# --------------------------- #

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------- #
# Authentification models
# --------------------------- #

# _ Firebase Admin
class FirebaseUserInformations(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField() # Email verified
    sign_in_provider = models.CharField(max_length=255) # Sign in provider
    # ---------------------------

    def __str__(self):
        return f"{self.user.username} - {self.email_verified} - {self.sign_in_provider}"
    
    class Meta:
        verbose_name = "Firebase User Informations"
        verbose_name_plural = "Firebase User Informations"
        unique_together = ('user', 'sign_in_provider')



# --------------------------- #
# Payment models
# --------------------------- #

class Subscription(BaseModel):
    PROVIDERS = [
        ('STRIPE', 'Stripe'), 
        ('LEMON', 'LemonSqueezy')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    provider = models.CharField(max_length=10, choices=PROVIDERS)
    subscription_id = models.CharField(max_length=255)
    plan_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50)


    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ('user', 'plan_id')



# --------------------------- #
# Stripe models
# --------------------------- #
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class StripeCustomerModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False, verbose_name=_("ID"))
    address = models.JSONField(null=True, blank=True, verbose_name=_("Address"))
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Description"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Name"))
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Phone"))
    shipping = models.JSONField(null=True, blank=True, verbose_name=_("Shipping"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    # ---------------------------

    class Meta:
        verbose_name = _("Stripe Customer")
        verbose_name_plural = _("Stripe Customers")
    
    def __str__(self):
        return self.name
    
    def get_subscriptions(self):
        return StripeSubscriptionModel.objects.filter(customer=self.id)
    
    def get_plans(self):
        plans = []
        for subscription in self.get_subscriptions():
            plans.append(subscription.get_plans())
        return plans
    
    def get_invoices(self):
        return StripeInvoiceModel.objects.filter(customer=self.id)


class StripeProductModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False, verbose_name=_("ID"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    default_price = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Default Price"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    object = models.CharField(max_length=50, verbose_name=_("Object Type"))
    created = models.DateTimeField(verbose_name=_("Created"))
    images = models.JSONField(default=list, blank=True, verbose_name=_("Images"))
    livemode = models.BooleanField(default=False, verbose_name=_("Live Mode"))
    marketing_features = models.JSONField(default=list, blank=True, verbose_name=_("Marketing Features"))
    package_dimensions = models.JSONField(null=True, blank=True, verbose_name=_("Package Dimensions"))
    shippable = models.BooleanField(null=True, blank=True, verbose_name=_("Shippable"))
    statement_descriptor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Statement Descriptor"))
    tax_code = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Tax Code"))
    unit_label = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Unit Label"))
    updated = models.DateTimeField(verbose_name=_("Updated"))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Stripe Product")
        verbose_name_plural = _("Stripe Products")
        ordering = ['-created']

    def __str__(self):
        return self.name
    
    def get_default_price(self):
        return StripePlanModel.objects.get(id=self.default_price)
    
    def get_plans(self):
        return StripePlanModel.objects.filter(product=self.id)
    
    def get_active_plans(self):
        return StripePlanModel.objects.filter(product=self.id, active=True)
    
    def get_inactive_plans(self):
        return StripePlanModel.objects.filter(product=self.id, active=False)
    
    def get_subscriptions(self):
        return StripeSubscriptionModel.objects.filter(product=self.id)


class StripePlanModel(models.Model):
    class Currency(models.TextChoices):
        USD = 'usd', _('US Dollar')
        EUR = 'eur', _('Euro')
        # Add more currencies here ...

    class Interval(models.TextChoices):
        DAY = 'day', _('Day')
        WEEK = 'week', _('Week')
        MONTH = 'month', _('Month')
        YEAR = 'year', _('Year')

    class BillingScheme(models.TextChoices):
        PER_UNIT = 'per_unit', _('Per Unit')
        TIERED = 'tiered', _('Tiered')

    class UsageType(models.TextChoices):
        METERED = 'metered', _('Metered')
        LICENSED = 'licensed', _('Licensed')

    id = models.CharField(max_length=255, primary_key=True, editable=False, verbose_name=_("ID"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    amount = models.IntegerField(null=True, blank=True, verbose_name=_("Amount"))
    amount_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Amount Decimal"))
    currency = models.CharField(max_length=3, choices=Currency.choices, verbose_name=_("Currency"))
    interval = models.CharField(max_length=10, choices=Interval.choices, verbose_name=_("Interval"))
    interval_count = models.IntegerField(default=1, verbose_name=_("Interval Count"))
    billing_scheme = models.CharField(max_length=20, choices=BillingScheme.choices, verbose_name=_("Billing Scheme"))
    created = models.DateTimeField(verbose_name=_("Created"))
    livemode = models.BooleanField(default=False, verbose_name=_("Live Mode"))
    metadata = models.JSONField(null=True, blank=True, verbose_name=_("Metadata"))
    nickname = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Nickname"))
    product = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Product ID"))
    tiers_mode = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Tiers Mode"))
    transform_usage = models.JSONField(null=True, blank=True, verbose_name=_("Transform Usage"))
    trial_period_days = models.IntegerField(null=True, blank=True, verbose_name=_("Trial Period Days"))
    usage_type = models.CharField(max_length=10, choices=UsageType.choices, default=UsageType.LICENSED, verbose_name=_("Usage Type"))

    def get_product(self):
        return StripeProductModel.objects.get(id=self.product)
    
    def get_subscriptions(self):
        return StripeSubscriptionModel.objects.filter(items__data__plan__id=self.id)

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = _("Stripe Plan")
        verbose_name_plural = _("Stripe Plans")
        ordering = ['-created']


class StripeSubscriptionModel(models.Model):
    class Status(models.TextChoices):
        INCOMPLETE = 'incomplete', _('Incomplete')
        INCOMPLETE_EXPIRED = 'incomplete_expired', _('Incomplete Expired')
        TRIALING = 'trialing', _('Trialing')
        ACTIVE = 'active', _('Active')
        PAST_DUE = 'past_due', _('Past Due')
        CANCELED = 'canceled', _('Canceled')
        UNPAID = 'unpaid', _('Unpaid')
        PAUSED = 'paused', _('Paused')

    id = models.CharField(max_length=255, primary_key=True, editable=False, verbose_name=_("ID"))
    cancel_at_period_end = models.BooleanField(default=False, verbose_name=_("Cancel at Period End"))
    currency = models.CharField(max_length=3, verbose_name=_("Currency"))
    current_period_end = models.DateTimeField(verbose_name=_("Current Period End"))
    current_period_start = models.DateTimeField(_("Current Period Start"))
    customer = models.CharField(max_length=255, verbose_name=_("Customer ID"))
    default_payment_method = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Default Payment Method"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    items = models.JSONField(verbose_name=_("Items"))
    latest_invoice = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Latest Invoice"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    pending_setup_intent = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Pending Setup Intent"))
    pending_update = models.JSONField(null=True, blank=True, verbose_name=_("Pending Update"))
    status = models.CharField(max_length=50, choices=Status.choices, verbose_name=_("Status"))
    # ---------------------------

    class Meta:
        verbose_name = _("Stripe Subscription")
        verbose_name_plural = _("Stripe Subscriptions")
        ordering = ['-current_period_end']
    
    def __str__(self):
        return self.id

    def get_customer(self):
        return User.objects.get(id=self.customer)
    
    def get_plans(self):
        print(self.items['data'].items())
        return StripePlanModel.objects.filter(id__in=[k['plan']['id'] for k, v in self.items['data'].items()])
    
    def get_latest_invoice(self):
        return StripeInvoiceModel.objects.get(id=self.latest_invoice)
    
    def get_pending_setup_intent(self):
        return StripeSetupIntentModel.objects.get(id=self.pending_setup_intent)
    
    def get_pending_update(self):
        return self.pending_update

    def get_status(self):
        return self.status

    def get_metadata(self):
        return self.metadata
    

class StripeInvoiceModel(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        OPEN = 'open', _('Open')
        PAID = 'paid', _('Paid')
        UNCOLLECTIBLE = 'uncollectible', _('Uncollectible')
        VOID = 'void', _('Void')

    id = models.CharField(max_length=255, primary_key=True, editable=False)
    auto_advance = models.BooleanField(default=False, verbose_name=_("Auto Advance"))
    currency = models.CharField(max_length=3, verbose_name=_("Currency"))
    current_period_end = models.DateTimeField(verbose_name=_("Current Period End"))
    current_period_start = models.DateTimeField(verbose_name=_("Current Period Start"))
    customer = models.CharField(max_length=255, verbose_name=_("Customer ID"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    lines = models.JSONField(verbose_name=_("Lines"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    status = models.CharField(max_length=50, choices=Status.choices, verbose_name=_("Status"))
    hosted_invoice_url = models.URLField(null=True, blank=True, verbose_name=_("Hosted Invoice URL"))
    subscription = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Subscription ID"))
    # ---------------------------

    class Meta:
        verbose_name = _("Stripe Invoice")
        verbose_name_plural = _("Stripe Invoices")
        ordering = ['-current_period_end']
    
    def __str__(self):
        return self.id

    def get_customer(self):
        return StripeCustomerModel.objects.get(id=self.customer)
    
    def get_lines(self):
        return self.lines
    
    def get_status(self):
        return self.status

    def get_metadata(self):
        return self.metadata
    
    def get_subscription(self):
        return Subscription.objects.get(id=self.subscription)
    

class StripeSetupIntentModel(models.Model):
    class Status(models.TextChoices):
        REQUIRES_PAYMENT_METHOD = 'requires_payment_method', _('Requires Payment Method')
        REQUIRES_CONFIRMATION = 'requires_confirmation', _('Requires Confirmation')
        REQUIRES_ACTION = 'requires_action', _('Requires Action')
        PROCESSING = 'processing', _('Processing')
        CANCELED = 'canceled', _('Canceled')
        SUCCEEDED = 'succeeded', _('Succeeded')

    id = models.CharField(max_length=255, primary_key=True, editable=False, verbose_name=_("ID"))
    client_secret = models.CharField(max_length=255, verbose_name=_("Client Secret"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    last_setup_error = models.JSONField(null=True, blank=True, verbose_name=_("Last Setup Error"))
    next_action = models.JSONField(null=True, blank=True, verbose_name=_("Next Action"))
    status = models.CharField(max_length=50, choices=Status.choices, verbose_name=_("Status"))
    usage = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Usage"))
    cancellation_reason = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Cancellation Reason"))
    created = models.DateTimeField(verbose_name=_("Created"))
    livemode = models.BooleanField(default=False, verbose_name=_("Live Mode"))
    metadata = models.JSONField(default=dict, blank=True, verbose_name=_("Metadata"))
    # ---------------------------

    class Meta:
        verbose_name = _("Stripe Setup Intent")
        verbose_name_plural = _("Stripe Setup Intents")
        ordering = ['-created']
    
    def __str__(self):
        return self.id

    def get_last_setup_error(self):
        return self.last_setup_error
    
    def get_next_action(self):
        return self.next_action
    
    def get_status(self):
        return self.status

    def get_usage(self):
        return self.usage