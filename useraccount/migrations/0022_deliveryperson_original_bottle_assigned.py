# Generated by Django 3.0.3 on 2021-11-14 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0021_moneytransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryperson',
            name='original_bottle_assigned',
            field=models.CharField(blank=True, default=0, max_length=20, null=True),
        ),
    ]