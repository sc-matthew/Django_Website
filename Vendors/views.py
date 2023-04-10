from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.views import View
from .models import Vendors
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
        error_message = self.validateCustomer(vendors)

        if not error_message:
            vendors.password = make_password(vendors.password)
            vendors.register()
            return redirect("vendor_homepage")
        else:
            data = {"error": error_message, "values": value}
            return render(request, "vd_signup.html", data)

    def validateCustomer(self, vendors):
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
                    return redirect("vendor_test")
            else:
                error_message = "Please check your email and password"
        else:
            error_message = "Please check your email and password"

        print(email, password)
        return render(request, "vd_login.html", {"error": error_message})


def logout(request):
    request.session.clear()
    return redirect("login")

class Test(View):
    def get(self, request):
        return render(request, "test.html", {})