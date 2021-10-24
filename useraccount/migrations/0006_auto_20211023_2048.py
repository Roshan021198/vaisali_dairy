# Generated by Django 3.0.3 on 2021-10-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0005_mainadmin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainadmin',
            old_name='emp_id',
            new_name='admin_id',
        ),
        migrations.AddField(
            model_name='deliveryperson',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mainadmin',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]