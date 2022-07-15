# Generated by Django 4.0.5 on 2022-07-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_order_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'card'), (2, 'transfer')], default=1, verbose_name='payment method'),
        ),
    ]