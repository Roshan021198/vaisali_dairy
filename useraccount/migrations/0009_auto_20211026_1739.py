# Generated by Django 3.0.3 on 2021-10-26 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0008_auto_20211026_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcation',
            name='from_delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='useraccount.Deliveryperson'),
        ),
    ]