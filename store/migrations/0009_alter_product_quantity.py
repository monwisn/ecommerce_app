# Generated by Django 4.2.5 on 2023-11-01 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_product_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="quantity",
            field=models.IntegerField(default=0),
        ),
    ]