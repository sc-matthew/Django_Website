# Generated by Django 4.1.7 on 2023-04-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Buyers", "0009_alter_order_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="customer_picture",
            field=models.ImageField(null=True, upload_to="uploads/profile/"),
        ),
    ]
