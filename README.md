# DRF Easily Saas

This package allows integration with Firebase and Supabase for authentication outside the Django context.

![Firebase Logo](https://miro.medium.com/max/300/1*R4c8lHBHuH5qyqOtZb3h-w.png)
![Supabase Logo](https://seeklogo.com/images/S/supabase-logo-DCC676FFE2-seeklogo.com.png)

## 1. Authentication Configuration

### Firebase configuration

Create your [Firebase](https://console.firebase.google.com/) database, then download the `.json` authentication file linked to your project.

- Go to `Project settings`
- Then go to the `Service accounts` section
- Select `Python` then download by clicking on `Generate new private key`
- Upload the `.json` file into your Django project

### Supabase configuration

Create your [Supabase](https://supabase.com/) project:

- Go to your Supabase project dashboard
- Navigate to `Settings` > `API`
- Copy your project URL and API keys (anon key and service_role key)

## 2. Django configuration

**Install authentication app in your project**

```bash
pip install drf-easily-saas
```

```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Insert this app
    'drf_easily_saas',
]
```

Add a Easily configuration

```python
EASILY= {
    'auth_provider': 'firebase', # Required
    'payment_provider': 'stripe', # Required
    'frontend_url': 'http://localhost:3000', # Required
    'firebase_config': {
        'import_users': True,
        "hot_reload_import": False,
        'config': {
            "type": "service_account",
            "project_id": "o-380604",
            "private_key_id": "7b9b5b20483ccbb91e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANAQEFAASCBKYwggSiAgEAAoIBAQC1Mv+HbJi7ObeG\nLGAhYXS7gf+O+9gMPYQWgM6KZqvd2dhvuqxyzqJYttz5o55YKBZTFDdY5Kped51f\nU273RylDA6\nWsbW9xyvgmVpbIbja29Lhc1H1Hymd4edFfDdee/d9LTF8g8QNHJ5LFx\n0DvORqNuNh0rM78sQS9l+g9PNdCoBTWxXE8BRvUCgYB2PXGAGCVDeesKxDyR3hwj\nVxR0un/5KMjJgpChhPBwNFLtar6WrgQVMYZomCwh9xjTAh/69lxtzaxJ+mvz3A8X\n1waeyUrsd+aBviq0Yz/6JVDghOkY5ZrptcR3Dg0hHLkEg0QLixmWebUQnZ6knW7z\n38m94Msowc2s2N6uYVE63g==\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-i7799@oting-380604.iam.gserviceaccount.com",
            "client_id": "106479259625371201589",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-i7799%-380604.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        },
    },
    
    # Alternative Supabase configuration
    # 'auth_provider': 'supabase',
    # 'supabase_config': {
    #     'url': 'https://your-project.supabase.co',
    #     'anon_key': 'your-anon-key',
    #     'service_role_key': 'your-service-role-key',
    #     'import_users': True,
    #     'hot_reload_import': False,
    # },
    'stripe_config': {
        'public_key': os.getenv('STRIPE_PUBLIC_KEY'),
        'secret_key': os.getenv('STRIPE_SECRET_KEY'),
        'webhook_verif_strategy': 'apikey',
        'subscription': {
            'payment_method_types': ['card', 'paypal'],
            'billing_address_collection': 'auto',
            'shipping_address_collection': {
                'allowed_countries': ['US', 'CA', 'FR'],
            },
            'automatic_tax': {'enabled': True},
        },
    },
}
```


**Configure custom authentication in rest framework**

For Firebase:
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'drf_easily_saas.auth.firebase.protect.FirebaseAuthentication',
],
```

For Supabase:
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'drf_easily_saas.auth.supabase.protect.SupabaseAuthentication',
],
```

**Sync all existing users from your authentication database**

For Firebase:
```bash
python3 manage.py syncfirebaseusers
```

For Supabase:
```bash
python3 manage.py syncsupabaseusers
```

---

Have fun with Firebase and Supabase Authentication! 🚀
