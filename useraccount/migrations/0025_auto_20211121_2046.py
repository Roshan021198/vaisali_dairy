# Generated by Django 3.0.3 on 2021-11-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0024_transcation_bottle_nums'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcation',
            name='from_delivery',
        ),
        migrations.AddField(
            model_name='transcation',
            name='deliveryPer_uid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transcation',
            name='delivery_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]