# Generated by Django 3.0.3 on 2021-11-14 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0022_deliveryperson_original_bottle_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainadmin',
            name='bottle_numbers',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]