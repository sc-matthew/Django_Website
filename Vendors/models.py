from django.db import models

# Create your models here.

class Vendors(models.Model):
    store_name = models.CharField(max_length=50)
    contact_person_first_name = models.CharField(max_length=50)
    contact_person_last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=300)
    store_picture = models.ImageField(upload_to="uploads/store/")
    qrcode_picture = models.ImageField(upload_to="uploads/qrcode/")
    last_update = models.DateTimeField(auto_now=True)