# Generated by Django 4.1.7 on 2023-04-29 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Vendors", "0010_products_v_vendor"),
    ]

    operations = [
        migrations.RemoveField(model_name="products_v", name="vendor",),
    ]
