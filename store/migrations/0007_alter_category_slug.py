# Generated by Django 4.2.5 on 2023-10-26 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_category_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=120),
        ),
    ]
