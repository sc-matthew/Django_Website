# Generated by Django 4.1.7 on 2023-04-10 13:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vendors",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=100)),
                ("store_name", models.CharField(max_length=50)),
                ("contact_person_first_name", models.CharField(max_length=50)),
                ("contact_person_last_name", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=10)),
                ("address", models.CharField(max_length=300)),
                ("store_picture", models.ImageField(upload_to="uploads/store/")),
                ("qrcode_picture", models.ImageField(upload_to="uploads/qrcode/")),
                ("last_update", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
