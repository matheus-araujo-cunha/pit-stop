# Generated by Django 4.0.6 on 2022-07-21 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=1)),
                ('categorie', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
