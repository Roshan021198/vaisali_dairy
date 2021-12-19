# Generated by Django 3.0.3 on 2021-11-14 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0020_auto_20211115_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='moneyTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_add', models.CharField(blank=True, max_length=50, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='money added date')),
                ('remaining_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='useraccount.Customer')),
            ],
        ),
    ]