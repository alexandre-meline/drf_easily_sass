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
