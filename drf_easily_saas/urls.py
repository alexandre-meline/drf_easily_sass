from django.urls import path, include

app_name = 'drf_easily_saas'

local_routes = [
    # path('auth/', include('drf_easily_auth.auth.urls')),
    path('payment/', include('drf_easily_saas.payment.urls')),
]

urlpatterns = [
    path('', include(local_routes)),
]