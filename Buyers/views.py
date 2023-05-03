from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from Buyers.models import Customer, Order
from Vendors.models import  Products_v, Category_v, Vendors
from django.urls import reverse
from django.views import View
from .middlewares.auth import auth_middleware
import datetime


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
        return redirect("homepage")

    def get(self, request):
        print(f"{request.get_full_path()}")
        return HttpResponseRedirect(f'store'+f"{request.get_full_path().split('buyers/')[1]}")
    
def product_search(request):
    query = request.GET.get('query')
    products = Products_v.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'products': products})


def store(request):
    cart = request.session.get("cart")
    if not cart:
        request.session["cart"] = {}
    vendors = Vendors.objects.all()  # Get all vendors
    vendor_product_dict = {}  # Dictionary to hold vendor IDs as keys and corresponding products as values

    # Iterate over vendors and get their available products based on their operational hours
    for vendor in vendors:
        if vendor.open_hour <= datetime.datetime.now().time() <= vendor.to_hour:  # Check if the vendor is currently open
            vendor_products = Products_v.get_product_by_owner(vendor.id)
            vendor_product_dict[vendor.id] = vendor_products

    # Filter products based on available vendors
    products = []
    for product_list in vendor_product_dict.values():
        products += product_list

    # If a category ID is specified, filter products by category
    categoryID = request.GET.get("category")
    if categoryID:
        products = [product for product in products if product.category_id == categoryID]

    # Prepare data dictionary for rendering the template
    data = {"products": products, "categories": Category_v.get_all_categories(), "cart": cart}

    return render(request, "index.html", data)


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
        postData = request.POST
        first_name = postData.get("firstname")
        last_name = postData.get("lastname")
        phone = postData.get("phone")
        email = postData.get("email")
        password = postData.get("password")
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
        customer_id = request.session.get("customer")
        customer = Customer.objects.get(id=customer_id)
        
        # set original_email to current email value
        customer.original_email = customer.email

        customer.first_name = postData["firstname"]
        customer.last_name = postData["lastname"]
        customer.phone = postData["phone"]
        customer.email = postData["email"]

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
    
class ProductDetailsView(View):
    def get(self, request, product_id):
        products = Products_v.objects.get(id=product_id)
        return render(request, "product_details.html", {"products": products})

    def post(self, request, product_id): #-> Handle product in product_details page
        products = Products_v.objects.get(id=product_id)
        customer = request.session.get("customer")
        products.liked_by.add(customer)
        return render(request, "product_details.html", {"products": products})

class Tracking(View):
    def get(self, request):
        with open("/Users/matthew/Documents/2602369_WAD/GitHub Project/SUB_BRANCH/API/ThailandPost.txt") as f:
            token = f.read().strip()
        print(token)
        context = {"token": token}
        return render(request, "tracking.html", context)


# def like_product(request):
#     customer_id = request.session.get("customer")
#     customer = Customer.objects.get(id=customer_id)

#     if request.method == "POST":
#         product_id = request.POST.get('product_id')
#         products = Products_v.objects.get(id=product_id)
        
#         if customer in products.liked_by.all():
#             products.liked_by.remove(customer)
#         else:
#             products.liked_by.add(customer)

#         like, created = Like.objects.get(customer=customer, id=product_id)

#         if not created:
#             if like.value == 'Like':
#                 like.value = 'Unlike'
#             else:
#                 like.value = 'Like'

#         like.save()

#         return redirect('product_details')
