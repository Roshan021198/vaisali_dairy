# Generated by Django 3.0.3 on 2021-10-17 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_delivery', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('id_proof', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='customerimg/')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transcation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_delivery', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('customer_approval', models.BooleanField(default=False)),
                ('remark', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('remark_date', models.DateTimeField(verbose_name='remark date')),
                ('final_approval', models.BooleanField(default=False)),
                ('connect_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useraccount.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Deliveryperson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_id', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('id_proof', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='deliveryboy/')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='delivery_boy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='useraccount.Deliveryperson'),
        ),
    ]