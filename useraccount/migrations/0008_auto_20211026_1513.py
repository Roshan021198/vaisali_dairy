# Generated by Django 3.0.3 on 2021-10-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0007_auto_20211025_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcation',
            name='remark_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='remark date'),
        ),
    ]
