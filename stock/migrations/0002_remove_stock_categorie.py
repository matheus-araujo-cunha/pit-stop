# Generated by Django 4.0.6 on 2022-07-22 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='categorie',
        ),
    ]