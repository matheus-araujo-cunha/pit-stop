# Generated by Django 4.0.6 on 2022-07-21 17:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(max_length=50)),
                ('warrant', models.IntegerField()),
                ('img', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='stock.stock')),
            ],
        ),
    ]