# Generated by Django 5.0.4 on 2024-04-28 10:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drf_easily_saas', '0002_alter_subscription_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user', 'plan_id')},
        ),
    ]
