# Generated by Django 3.0.3 on 2021-10-25 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0006_auto_20211023_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='sign_up_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='sign_up_date'),
        ),
        migrations.AddField(
            model_name='deliveryperson',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_joined'),
        ),
    ]
