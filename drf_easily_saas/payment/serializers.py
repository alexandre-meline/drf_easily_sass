from rest_framework import serializers
from drf_easily_saas.models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = '__all__'