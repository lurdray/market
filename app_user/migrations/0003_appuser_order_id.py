# Generated by Django 3.1.3 on 2021-01-31 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_appuser_delivery_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='order_id',
            field=models.CharField(default='03inim4f', max_length=500),
        ),
    ]
