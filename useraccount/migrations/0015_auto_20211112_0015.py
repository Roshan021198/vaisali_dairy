# Generated by Django 3.0.3 on 2021-11-11 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0014_deliveryperson_bottle_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainadmin',
            name='assigned_bottle',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]
