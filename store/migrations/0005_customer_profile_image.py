# Generated by Django 4.2.5 on 2023-10-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_customer_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="profile_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="uploads/profile_image/"
            ),
        ),
    ]
