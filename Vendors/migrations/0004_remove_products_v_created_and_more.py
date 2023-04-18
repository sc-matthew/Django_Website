# Generated by Django 4.1.7 on 2023-04-14 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Vendors", "0003_rename_category_category_v_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="products_v", name="created",),
        migrations.AlterField(
            model_name="products_v",
            name="description",
            field=models.CharField(blank=True, default="", max_length=2500, null=True),
        ),
    ]