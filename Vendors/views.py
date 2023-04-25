from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views import View
from .models import Vendors,Products_v, Category_v
from .middlewares.auth import auth_middleware

class Homepage(View):
    def get(self, request):
        return render(request, 'vd_landing.html', {})

class Signup(View):
    def get(self, request):
        return render(request, "vd_signup.html")

    def post(self, request):
        postData = request.POST
        postFiles = request.FILES
        email = postData.get("email")
        password = postData.get("password")
        store_name = postData.get("storename")
        first_name = postData.get("firstname")
        last_name = postData.get("lastname")
        phone = postData.get("phone")
        address = postData.get("address")
        store_picture = postFiles.get("store_picture")
        qrcode_picture = postFiles.get("qrcode_picture")
        
        # validation
        value = {
            "email" : email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "store_name" : store_name,
            "address" : address,
        }
        error_message = None

        vendors = Vendors(
            email = email,
            password = password,
            store_name =  store_name,
            contact_person_first_name = first_name,
            contact_person_last_name = last_name,
            phone = phone,
            address = address,
            store_picture = store_picture,
            qrcode_picture = qrcode_picture
        )
        error_message = self.validateVendors(vendors)

        if not error_message:
            vendors.password = make_password(vendors.password)
            vendors.register()
            return redirect("vendor_homepage")
        else:
            data = {"error": error_message, "values": value}
            return render(request, "vd_signup.html", data)

    def validateVendors(self, vendors):
        error_message = None
        if not vendors.contact_person_first_name:
            error_message = "Please Enter your First Name !!"
        elif len(vendors.contact_person_first_name) < 3:
            error_message = "First Name must be 3 char long or more"
        elif not vendors.contact_person_last_name:
            error_message = "Please Enter your Last Name"
        elif len(vendors.contact_person_last_name) < 3:
            error_message = "Last Name must be 3 char long or more"
        elif not vendors.phone:
            error_message = "Enter your Phone Number"
        elif len(vendors.phone) < 10:
            error_message = "Phone Number must be 10 char Long"
        elif len(vendors.password) < 5:
            error_message = "Password must be 5 char long"
        elif len(vendors.email) < 5:
            error_message = "Email must be 5 char long"
        elif vendors.isExists():
            error_message = "Email Address Already Registered.."
        # saving

        return error_message
    
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get("return_url")
        return render(request, "vd_login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        vendors = Vendors.get_vendors_by_email(email)
        error_message = None
        if vendors:
            flag = check_password(password, vendors.password)
            if flag:
                request.session["vendors"] = vendors.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect("vendor_products")
            else:
                error_message = "Please check your email and password"
        else:
            error_message = "Please check your email and password"

        print(email, password)
        return render(request, "vd_login.html", {"error": error_message})


def logout(request):
    request.session.clear()
    return redirect("vendor_homepage")

class Account(View):
    def get(self, request):
        vendors = request.session.get("vendors")
        details = Vendors.get_vendors_by_vendorsid(vendors)
        return render(request, "vd_account_details.html", {"details" : details})
    
    def post(self, request):
        postData = request.POST
        vendors_id = request.session.get("vendors")
        vendors = Vendors.objects.get(id=vendors_id)
        
        # set original_email to current email value
        vendors.original_email = vendors.email

        vendors.store_name = postData["storename"]
        vendors.contact_person_first_name = postData["firstname"]
        vendors.contact_person_last_name = postData["lastname"]
        vendors.phone = postData["phone"]
        vendors.email = postData["email"]
        vendors.address = postData["address"]

        error_message = self.validateVendors(vendors)

        if not error_message:
            vendors.save()
            success_message = "Changes saved successfully!"
            return render(request, "vd_account_details.html", {"success_message": success_message, "details" : vendors})

        else:
            data = {"error": error_message, "details": vendors}
            return render(request, "vd_account_details.html", data)

    def validateVendors(self, vendors):
        error_message = None
        if not vendors.contact_person_first_name:
            error_message = "Please Enter your First Name !!"
        elif len(vendors.contact_person_first_name) < 3:
            error_message = "First Name must be 3 char long or more"
        elif not vendors.contact_person_last_name:
            error_message = "Please Enter your Last Name"
        elif len(vendors.contact_person_last_name) < 3:
            error_message = "Last Name must be 3 char long or more"
        elif not vendors.phone:
            error_message = "Enter your Phone Number"
        elif len(vendors.phone) < 10:
            error_message = "Phone Number must be 10 char Long"
        elif len(vendors.password) < 5:
            error_message = "Password must be 5 char long"
        elif len(vendors.email) < 5:
            error_message = "Email must be 5 char long"
        elif vendors.email != vendors.original_email and vendors.isExists():
            error_message = "Email Address Already Registered.."
        # saving

        return error_message
    
class Image(View):
    def get(self, request):
        vendors = request.session.get("vendors")
        details = Vendors.get_vendors_by_vendorsid(vendors)
        print(details)
        return render(request, "vd_account_image.html", {"details" : details})
    
    def post(self, request):
        postFiles = request.FILES
        vendors_id = request.session.get("vendors")
        vendors = Vendors.objects.get(id=vendors_id)

        store_picture = postFiles.get("store_picture")
        qrcode_picture = postFiles.get("qrcode_picture")

        # Check file types
        if store_picture.content_type != "image/jpeg":
            error_message = "Invalid file type for Store Picture (Only JPEG and JPG are supported). Please try again."
            return render(request, "vd_account_image.html", {"error_message": error_message, "details": vendors})
        
        elif qrcode_picture.content_type != "image/jpeg":
            error_message = "Invalid file type for QRCode Picture (Only JPEG and JPG are supported). Please try again."
            return render(request, "vd_account_image.html", {"error_message": error_message, "details": vendors})

        vendors.store_picture = store_picture
        vendors.qrcode_picture = qrcode_picture
        
        vendors.save()
        success_message = "Changes saved successfully!"
        return render(request, "vd_account_image.html", {"success_message": success_message, "details" : vendors})


class vendor_store(View):
    def get(self, request):
        products = None
        categories = Category_v.get_all_categories()
        categoryID = request.GET.get("category")
        if categoryID:
            products = Products_v.objects.filter(ownerid=request.session.get("vendors")).filter(category=categoryID)
        else:
            products = Products_v.get_product_by_owner(request.session.get("vendors"))

        data = {}
        data["products"] = products
        data["categories"] = categories

        return render(request, "vd_products.html",data)

class AddProduct(View):
    def get(self, request):
        categories = Category_v.get_all_categories()
        categoryID = request.GET.get("category")

        return render(request, 'vd_add_product.html', {"categories": categories, "categoryID": categoryID})

    def post(self, request):
        postData = request.POST
        postFiles = request.FILES
        name = postData.get("name")
        price = postData.get("price")
        category_id = postData.get('category')
        category = Category_v.get_category_by_categorysid(category_id)
        description = postData.get("description")
        image = postFiles.get("image")
        status = postData.get("status")
        owner = request.session.get("vendors")
        if status == 'on':
            status = 1
        else:
            status = 0
        
        product = Products_v(
            name = name,
            price = price,
            description = description,
            image = image,
            category_id = category_id,
            status = status,
            ownerid = owner
        )
            
        if image.content_type != "image/jpeg":
            error_message = "Invalid file type for Store Picture (Only JPEG and JPG are supported). Please try again."
            data = {"error": error_message, "values": product}
            return render(request, "vd_add_product.html", data)
        else:
            error_message = self.validateProduct(product)

            if not error_message:
                product.save()
                success_message = "Changes saved successfully!"
                return render(request, "vd_add_product.html", {"success_message": success_message, "values": product})
            else:
                data = {"error": error_message, "values": product}
                return render(request, "vd_signup.html", data)
        
    def validateProduct(self, product):
        error_message = None
        if len(product.description.strip()) == 0:
            error_message = "You should not enter blank in the description"

        return error_message


class EditProduct(View):
    def get(self, request, product_id):
        product = Products_v.objects.get(id=product_id)
        categories = Category_v.get_all_categories()
        print(product.name, product.description, product.price, product.category_id)
        return render(request, "vd_edit_product.html", {"details":product, "categories":categories})

class AddCategory(View):
    def get(self, request):
        return render(request, "vd_add_category.html")
    
    def post(self, request):
        postData = request.POST
        name = postData.get('name')


        # Convert the category name to lowercase
        lowercase_name = name.lower()

        category = Category_v(
            name=name
        )

        if Category_v.objects.filter(name__iexact=lowercase_name).exists():
            error_message = "This category name already exists."
            data = {"error_message": error_message, "name": name}
            return render(request, "vd_add_category.html", data)

        category = Category_v(name=name)
        success_message = "Changes saved successfully!"
        category.save()
        return redirect("add_product")
        
    
class EditCategory(View):
    def get(self, request):
        category_id = request.GET.get('category')
        category = Category_v.get_category_by_categorysid(category_id)
        return render(request, 'vd_edit_category.html', {'category': category})

    def post(self, request):
        category_id = int(request.GET.get('category'))
        category = Category_v.get_category_by_categorysid(category_id) 
        

        if category is not None:
            name = request.POST.get('name')
            lowercase_name = name.lower()

            if Category_v.objects.filter(name__iexact=lowercase_name).exclude(id=category_id).exists():
                error_message = "This category name already exists."
                data = {"error_message": error_message, "name": name}
                return render(request, "vd_edit_category.html", data)

            category.name = name
            success_message = "Changes saved successfully!"
            category.save()
            return render(request, "vd_edit_category.html", {'success_message':success_message})
    



