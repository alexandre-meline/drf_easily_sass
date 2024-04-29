# DRF Firebase Auth

This package allows integration with Firebase for authentication outside the Django context.

![Firebase Logo](https://miro.medium.com/max/300/1*R4c8lHBHuH5qyqOtZb3h-w.png)

## 1. Firebase configuration

Create your [Firebase](https://console.firebase.google.com/) database, then download the `.json` authentication file linked to your project.

- Go to `Project settings`
- Then go to the `Service accounts` section
- Select `Python` then download by clicking on `Generate new private key`
- Upload the `.json` file into your Django project

## 2. Django configuration

**Install authentication app in your project**

```bash
pip install drf-easily-auth
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
    'drf_easily_auth',
]
```

Add a Firebase configuration

```bash
FIREBASE_CONFIG_FILE = # Your Firebase config file path downloaded in step 1
```

Or

```bash
FIREBASE_CONFIG_FILE = {
  apiKey: "AIqdqdymodlwEXOOdddVbacklbBXrNjwu6Mg",
  authDomain: "oting-38060qddqdq4.firebaseapp.com",
  projectId: "oting-3806dqdqdq04",
  storageBucket: "oting-380604.appspt.com",
  messagingSenderId: "3430090dqd20511",
  appId: "1:343009511:web:e49dqdqd421ed29ea"
}
```


**Configure custom Firebase authentication in rest framework**

```bash
'DEFAULT_AUTHENTICATION_CLASSES': [
    'drf_easily_auth.firebase.auth.FirebaseAuthentication',
],
```

**Sync all existing users from your Firebase database**

```bash
python3 manage.py syncfirebaseusers
```

---

Have fun with Firebase Authentication! 🚀
