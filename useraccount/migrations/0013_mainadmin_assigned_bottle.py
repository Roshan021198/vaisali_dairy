# Generated by Django 3.0.3 on 2021-11-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0012_auto_20211111_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainadmin',
            name='assigned_bottle',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
