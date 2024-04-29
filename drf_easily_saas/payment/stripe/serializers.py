from rest_framework import serializers


# For the request
class CheckoutSerializer(serializers.Serializer):
    price_id = serializers.CharField(max_length=200)
    uid = serializers.CharField(max_length=50)
    user_email = serializers.EmailField()
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()
    metadata = serializers.DictField(required=False)

    class Meta:
        fields = '__all__'
        # return in response only these fields

# For the response
class CheckoutSessionSerializer(serializers.Serializer):
    id = serializers.CharField()
    mode = serializers.CharField(max_length=50, default='subscription')
    url = serializers.URLField()
    client_reference_id = serializers.CharField(max_length=50)
    customer_email = serializers.EmailField()
    customer_details = serializers.DictField()
    status = serializers.CharField(max_length=50)
    cancel_url = serializers.URLField()
    success_url = serializers.URLField()
    metadata = serializers.DictField()

    class Meta:
        fields = '__all__'
        # return in response only these fields