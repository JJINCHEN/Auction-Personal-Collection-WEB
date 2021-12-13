from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
import re


# Create your views here.

# Buyer user registration page Jump
def buy_register(request):
    try:
        msg = ""
        if request.method == "GET":
            return render(request, "buyregister.html", locals())
    except Exception as e:
        print(e)
        msg = "Add failed, system error"
        return render(request, "buyregister.html", locals())


# Judgment of buyer user registration
def do_buy_register(request):
    try:
        msg = ""
        # Judgment of submission form
        if request.method == "POST":
            # Data filled in advance
            user = request.user
            datas = request.POST
            username = request.POST.get("username")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            mtype = request.POST.get("mtype", "")
            email = request.POST.get("email", "")
            address = request.POST.get("address", "")

            # Show incoming data
            # print("=====")
            # print(username)
            # print(password)
            # print(password2)
            # print(mtype)
            # print(email)
            # print(address)

            return_page = "buyregister.html"

            # Address writing requirements
            if address != "":
                if len(address) < 6:
                    msg = "The address must be greater than 6 digits"
                    return render(request, return_page, locals())
            # Determine whether the mailbox conforms to the regular expression format
            if re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,19}.com', email) == None:
                msg = "The Email format is incorrect"
                return render(request, return_page, locals())
            # Judge whether the two passwords are the same
            if password != password2:
                msg = "The two passwords are inconsistent"
                return render(request, return_page, locals())
            # Judge that the number of digits of user name and password is greater than the specified 6 digits
            if len(username) < 6 or len(password) < 6 or len(password2) < 6:
                msg = "The password and username must be greater than 6 digits"
                return render(request, return_page, locals())

            # Judge whether the user name exists
            only = UserProfile.objects.filter(username=username)
            # Judge whether the user name exists, and display the prompt
            if len(only) > 0:
                msg = "The user name already exists"
                return render(request, return_page, locals())
            # When there is a problem in user registration, there are not two kinds of user judgments.
            # If do not manually modify the database, it will not appear now
            if mtype not in ["0", "1"]:
                msg = "Only buyers or sellers can register"
                return render(request, return_page, locals())

            # Judge whether the user exists
            email_user = UserProfile.objects.filter(email=email)
            # Judge whether the email exists, and display the prompt
            if len(email_user) > 0:
                msg = "Email cannot be repeated!"
                return render(request, return_page, locals())
            # Add new users to the database
            new_user = UserProfile()
            new_user.username = username
            new_user.email = email
            new_user.address = address
            new_user.set_password(password)
            new_user.mtype = int(mtype)
            new_user.save()
            # Jump to login page
            return redirect("accounts:login")
        else:
            # Register have some error, jump back to register page
            return render(request, "buyregister.html", locals())
    # Failed to add user, and prompt
    except Exception as e:
        print(e)
        msg = "Add failed, system error"
        return render(request, "buyregister.html", locals())


# Seller user registration page Jump
def sell_register(request):
    try:
        msg = ""
        if request.method == "GET":
            return render(request, "sellregister.html", locals())
    except Exception as e:
        print(e)
        msg = "Add failed, system error"
        return render(request, "sellregister.html", locals())


# Judgment of seller registration
def do_sell_register(request):
    try:
        msg = ""
        # Judgment of submission form
        if request.method == "POST":
            user = request.user
            datas = request.POST
            # Data filled in advance
            username = request.POST.get("username")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            mtype = request.POST.get("mtype", "")
            email = request.POST.get("email", "")
            bank_no = request.POST.get("bank_no", "")
            agree = request.POST.get("agree", "")

            return_page = "sellregister.html"
            # Judge whether the contract is agreed or not
            if agree != "on":
                msg = "You must agree to the contract to register"
                return render(request, return_page, locals())
            # Determine whether the mailbox conforms to the regular expression format
            if re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,19}.com', email) == None:
                msg = "The Email format is incorrect"
                return render(request, return_page, locals())
            # Judge whether the two passwords are the same
            if password != password2:
                msg = "The two passwords are inconsistent"
                return render(request, return_page, locals())
            # Judge that the number of bank cards entered is 16
            if bank_no != "" and len(bank_no) != 16:
                msg = "Bank card number must be  16 digits"
                return render(request, return_page, locals())
            # Judge that the number of digits of user name and password is greater than the specified 6 digits
            if len(username) < 6 or len(password) < 6 or len(password2) < 6:
                msg = "The password and username must be greater than 6 digits"
                return render(request, return_page, locals())
            # Judge whether the user name exists
            only = UserProfile.objects.filter(username=username)
            # Determine whether the user name exists
            if len(only) > 0:
                msg = "The user name already exists"
                return render(request, return_page, locals())

            # When there is a problem in user registration, there are not two kinds of user judgments.
            # If do not manually modify the database, it will not appear now
            if mtype not in ["0", "1"]:
                msg = "Only buyers or sellers can register"
                return render(request, return_page, locals())

            # Judge whether the user exists
            email_user = UserProfile.objects.filter(email=email)
            # Judge whether the email exists, and display the prompt
            if len(email_user) > 0:
                msg = "Email cannot be repeated!"
                return render(request, return_page, locals())
            # Add new users to the database
            new_user = UserProfile()
            new_user.username = username
            new_user.email = email
            new_user.bank_no = bank_no
            new_user.set_password(password)
            new_user.mtype = int(mtype)
            new_user.save()
            # Jump to login page
            return redirect("accounts:login")
        else:
            # Register have some error, jump back to register page
            return render(request, "sellregister.html", locals())
    # Failed to add user, and prompt
    except Exception as e:
        print(e)
        msg = "Add failed, system error"
        return render(request, "sellregister.html", locals())


# User login
def user_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("/")
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    # user.backend = 'django.contrib.auth.backends.ModelBackend' # Specify the default login authentication method
                    login(request, user)
                else:
                    return render(request, 'errinfo.html')
                return render(request, 'succ.html')
            else:
                return render(request, 'errinfo.html')
        else:
            login_form = LoginForm()
            return render(request, 'login.html', {'login_form': login_form})
    except Exception as e:
        login_form = LoginForm()
        print(e)
        return render(request, 'errinfo.html')


# User logout
@login_required
def user_logout(request):
    try:
        logout(request)
        return redirect('accounts:login')
    except Exception as e:
        print(e)
    return render(request, "error.html", {"msg": "Exit error"})
