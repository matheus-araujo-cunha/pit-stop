# Generated by Django 4.0.6 on 2022-07-22 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_users_order_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='users',
            new_name='user',
        ),
    ]