# Generated by Django 3.0.3 on 2021-12-01 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0030_auto_20211128_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneytransaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='moneytransaction',
            name='transaction_registered_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='moneytransaction',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
