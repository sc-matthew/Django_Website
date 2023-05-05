from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from Buyers.models import Customer, Order
from Vendors.models import  Products_v, Category_v, Vendors
from django.urls import reverse
from django.views import View
from .middlewares.auth import auth_middleware
import datetime
import os
from dotenv import load_dotenv, dotenv_values


# Create your views here.


class Cart(View):
    def get(self, request):
        ids = list(request.session.get("cart").keys())
        products = Products_v.get_products_by_id(ids)
        print(products)
        return render(request, "cart.html", {"products": products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get("customer")
        cart = request.session.get("cart")
        products = Products_v.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id)),
            )
            order.save()
        request.session["cart"] = {}

        return redirect("cart")

class Index(View):
    def get(self, request):
        print(f"1.{request.get_full_path()}")
        return HttpResponseRedirect(f'store'+f"{request.get_full_path().split('buyers/')[1]}")
    
    def post(self, request):
        product = request.POST.get("product")
        remove = request.POST.get("remove")
        cart = request.session.get("cart")
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session["cart"] = cart
        print("cart", request.session["cart"])
        print(f"{request.get_full_path()}")
        return redirect("homepage")

def store(request):
    all_vendors = Vendors.get_all_vendor()
    cart = request.session.get("cart")
    if not cart:
        request.session["cart"] = {}

    # Get all vendors that are currently open
    open_vendors = Vendors.objects.filter(open_hour__lte=datetime.datetime.now().time(),
                                           to_hour__gte=datetime.datetime.now().time())

    # Get the products of the open vendors
    vendor_product_dict = {}
    for vendor in open_vendors:
        vendor_products = Products_v.get_product_by_owner(vendor.id)
        vendor_product_dict[vendor.id] = vendor_products

    # If a category ID is specified, filter products by category from the open vendors
    categories = Category_v.get_all_categories()
    categoryID = request.GET.get("category")
    if categoryID:
        products = []
        for vendor_id, product_list in vendor_product_dict.items():
            filtered_products = product_list.filter(category=categoryID)
            if filtered_products:
                products += filtered_products
    else:
        # Get all products from the open vendors
        products = []
        for product_list in vendor_product_dict.values():
            products += product_list

    # Prepare data dictionary for rendering the template
    data = {"products": products, "categories": categories, "cart": cart, "all_vendors": all_vendors}
    print(f'2.{request.get_full_path()}')
    return render(request, "index.html", data)

def product_search(request):
    all_vendors = Vendors.get_all_vendor()
    cart = request.session.get("cart")
    if not cart:
        request.session["cart"] = {}
    vendors = Vendors.objects.all()
    vendor_product_dict = {} 

    for vendor in vendors:
        if vendor.open_hour <= datetime.datetime.now().time() <= vendor.to_hour:  # Check if the vendor is currently open
            vendor_products = Products_v.get_product_by_owner(vendor.id)
            vendor_product_dict[vendor.id] = vendor_products

    query = request.GET.get('query')
    products = Products_v.objects.filter(name__icontains=query)
    data = {"products": products, "cart": cart, "all_vendors" : all_vendors}
    return render(request, 'search.html',  data)

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get("return_url")
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session["customer"] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect("store")
            else:
                error_message = "Please check your email and password"
        else:
            error_message = "Please check your email and password"

        print(email, password)
        return render(request, "login.html", {"error": error_message})


def logout(request):
    request.session.clear()
    return redirect("login")

class OrderView(View):
    def get(self, request):
        customer = request.session.get("customer")
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, "orders.html", {"orders": orders})


class Signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        postFiles = request.FILES
        postData = request.POST
        first_name = postData.get("firstname")
        last_name = postData.get("lastname")
        phone = postData.get("phone")
        email = postData.get("email")
        password = postData.get("password")
        profile_picture = postFiles.get("profile_picture")
        # validation
        value = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
        }
        error_message = None

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password,
            profile_picture=profile_picture,
        )
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect("homepage")
        else:
            data = {"error": error_message, "values": value}
            return render(request, "signup.html", data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = "First Name must be 3 char long or more"
        elif not customer.last_name:
            error_message = "Please Enter your Last Name"
        elif len(customer.last_name) < 3:
            error_message = "Last Name must be 3 char long or more"
        elif not customer.phone:
            error_message = "Enter your Phone Number"
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 char Long"
        elif len(customer.password) < 5:
            error_message = "Password must be 5 char long"
        elif len(customer.email) < 5:
            error_message = "Email must be 5 char long"
        elif customer.isExists():
            error_message = "Email Address Already Registered.."
        # saving

        return error_message

class Account(View):
    def get(self, request):
        customer = request.session.get("customer")
        details = Customer.get_customer_by_customerid(customer)
        return render(request, "account.html", {"details" : details})
    
    def post(self, request):
        postData = request.POST
        postFiles = request.FILES
        customer_id = request.session.get("customer")
        customer = Customer.objects.get(id=customer_id)
        
        # set original_email to current email value
        customer.original_email = customer.email

        customer.first_name = postData["firstname"]
        customer.last_name = postData["lastname"]
        customer.phone = postData["phone"]
        customer.email = postData["email"]

        if 'profile_picture' in postFiles:
            profile_picture = postFiles.get("profile_picture")
            if profile_picture.content_type != "image/jpeg":
                error = "Invalid file type for Profile Picture (Only JPEG and JPG are supported). Please try again."
                return render(request, "account.html", {"error": error, "details": customer})
            customer.profile_picture = profile_picture

        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.save()
            success_message = "Changes saved successfully!"
            return render(request, "account.html", {"success_message": success_message, "details" : customer})

        else:
            data = {"error": error_message, "details": customer}
            return render(request, "account.html", data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = "First Name must be 3 char long or more"
        elif not customer.last_name:
            error_message = "Please Enter your Last Name"
        elif len(customer.last_name) < 3:
            error_message = "Last Name must be 3 char long or more"
        elif not customer.phone:
            error_message = "Enter your Phone Number"
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 char Long"
        elif len(customer.email) < 5:
            error_message = "Email must be 5 char long"
        elif customer.email != customer.original_email and customer.isExists():
            error_message = "Email Address Already Registered.."
        
        return error_message
    
class Profile(View):
    def get(self, request):
        customer = request.session.get("customer")
        details = Customer.get_customer_by_customerid(customer)
        return render(request, "buyer_profile.html", {"details" : details})
    
class ProductDetailsView(View):
    def get(self, request, product_id):
        products = Products_v.objects.get(id=product_id)
        vendor = Vendors.objects.get(id=products.ownerid)
        return render(request, "product_details.html", {"product": products, "vendor":vendor})

    def post(self, request, product_id):
        products = Products_v.objects.get(id=product_id)
        vendor = Vendors.objects.get(id=products.ownerid)
        product = request.POST.get("product")
        remove = request.POST.get("remove")
        cart = request.session.get("cart")
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session["cart"] = cart
        print("cart", request.session["cart"])
        return render(request, "product_details.html", {"product": products, "vendor":vendor})

class VendorDetail_onBuyers(View):
    def get(self, request, vendorid):
        vendor = Vendors.get_vendors_by_vendorsid(vendorid)
        vendor_store = vendor.store_name.lower().replace(" ","")
        num_product = len(Products_v.objects.filter(ownerid=vendorid))
        open_hour = vendor.open_hour.strftime("%H:%M")
        to_hour = vendor.to_hour.strftime("%H:%M")
        print(open_hour, to_hour)

        config = {
                    **dotenv_values(".env.secret")
                }

        api = config['GOOGLE_API_KEY']

        data = {"vendor":vendor, "vendor_store":vendor_store, "num_product" : num_product, "api" : api,
                "open_hour":open_hour, "to_hour":to_hour}

        return render(request, "seller_profile.html", data)
    
class Tracking(View):
    def get(self, request):
        config = {
                    **dotenv_values(".env.secret")
                }

        token = config['THAILAND_POST_TOKEN']
        return render(request, "tracking.html", {"token": token})

