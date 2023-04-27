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

class Category_v(models.Model):
    name = models.CharField(max_length=50, unique = True)

    @staticmethod
    def register(self):
        self.save()
        
    def get_all_categories():
        return Category_v.objects.all()

    def get_category_by_categorysid(category_id):
        try:
            return Category_v.objects.get(id=category_id)
        except Category_v.DoesNotExist:
            return None

    def __str__(self):
        return self.name
    

class Products_v(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category_v, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=2500)
    image = models.ImageField(upload_to="uploads/products/")
    status = models.BooleanField(default=True)
    ownerid = models.PositiveSmallIntegerField(default=1, null=False)
    last_update = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_products_by_id(ids):
        return Products_v.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products_v.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products_v.objects.filter(category=category_id)
        else:
            return Products_v.get_all_products()
        
    def get_product_by_owner(ownerid):
        if ownerid:
            return Products_v.objects.filter(ownerid=ownerid)
        else:
            return None
