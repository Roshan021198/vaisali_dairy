# Generated by Django 3.0.3 on 2021-11-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0013_mainadmin_assigned_bottle'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryperson',
            name='bottle_assigned',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
