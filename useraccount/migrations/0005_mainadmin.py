# Generated by Django 3.0.3 on 2021-10-23 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mainadmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_id', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=500, null=True)),
                ('id_proof', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='adminimg/')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
