# Generated by Django 3.0.3 on 2021-11-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0009_auto_20211026_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcation',
            name='final_message',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
