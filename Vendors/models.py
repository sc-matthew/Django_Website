from django.db import models

# Create your models here.

class Vendors(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    store_name = models.CharField(max_length=50)
    contact_person_first_name = models.CharField(max_length=50)
    contact_person_last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=300)
    store_picture = models.ImageField(upload_to="uploads/store/")
    qrcode_picture = models.ImageField(upload_to="uploads/qrcode/")
    last_update = models.DateTimeField(auto_now=True)

    # to save the data
    def register(self):
        self.save()

    @staticmethod
    def get_vendors_by_email(email):
        try:
            return Vendors.objects.get(email=email)
        except:
            return False
        
    def get_vendors_by_vendorsid(vendors_id):
        try:
            return Vendors.objects.get(id=vendors_id)
        except Vendors.DoesNotExist:
            return None
        
    def isExists(self):
        if Vendors.objects.filter(email=self.email):
            return True

        return False