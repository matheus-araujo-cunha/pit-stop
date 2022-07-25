# Generated by Django 4.0.6 on 2022-07-25 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_warrant_products_warranty'),
        ('carts', '0003_remove_cart_products_cartproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='carts', through='carts.CartProduct', to='products.products'),
        ),
        migrations.DeleteModel(
            name='CartProducts',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products'),
        ),
    ]