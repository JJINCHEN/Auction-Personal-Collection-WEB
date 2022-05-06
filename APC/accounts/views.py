from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from sell.models import Product, Category, BuyPrice, Order, TransferMoney
from django.contrib.auth.hashers import make_password, check_password
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
            return render(request, "login.html", {"msg": "Register successful"})
        else:
            # Register have some error, jump back to register page
            return render(request, "buyregister.html", {"msg": "Register error"})
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
            return render(request, "login.html", {"msg": "Register successful"})
        else:
            # Register have some error, jump back to register page
            return render(request, "sellregister.html", locals())
    # Failed to add user, and prompt
    except Exception as e:
        print(e)
        msg = "Add failed, system error"
        return render(request, "sellregister.html", {"msg": "Register error"})


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
                    errorinfo = "Incorrect account or password"
                    return render(request, 'login.html', {'login_form': login_form, "msg": errorinfo})
                if user.mtype == 2:
                    return redirect("/statistics_index")
                return redirect("/")
            else:
                errorinfo = "Incorrect account or password"
                return render(request, 'login.html', {'login_form': login_form, "msg": errorinfo})
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


# The judgment of modifying the buyer's password
def modify_buy_password(request):
    # Confirm user
    user = request.user
    categories = Category.objects.filter()
    products = BuyPrice.objects.filter(user=user).values("product")
    orders = Order.objects.filter(user=user)
    try:
        # Judge the form
        if request.method == "POST":
            user = request.user
            datas = request.POST
            # Extract form input
            old_password = request.POST.get("old_password")
            pwd1 = request.POST.get("pwd1")
            pwd2 = request.POST.get("pwd2")
            # Show incoming data
            # print("===")
            # print(old_password)
            # print(pwd1)
            # print(pwd2)

            if len(old_password) < 6 or len(pwd1) < 6 or len(pwd2) < 6:
                msg = "The password must be greater than 6 digits"
                return render(request, "buy_userinfo.html", locals())
            if pwd1 != pwd2:
                msg = "The two passwords are inconsistent"
                return render(request, "buy_userinfo.html", locals())
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user no longer exists"
                return render(request, "buy_userinfo.html", locals())
            only = only[0]
            # Show incoming data
            # print(only.password)
            # print(make_password(old_password))

            if check_password(old_password, only.password) == False:
                msg = "The old password is incorrect"
                return render(request, "buy_userinfo.html", locals())
            only.password = make_password(pwd1)
            only.save()
            msg = "Modified successfully"
            return redirect("/buy_userinfo")
        else:
            msg = "Request error"
            return render(request, "buy_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        return render(request, "buy_userinfo.html", locals())


# The judgment of modifying address
def address(request):
    # Confirm user
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        # Judge the form
        if request.method == "POST":
            user = request.user
            datas = request.POST
            # Extract form input
            address = request.POST.get("address")
            # Judge that the input address must be greater than 6 digits
            if len(address) < 6:
                msg = "The address must be greater than six digits"
                return render(request, "buy_userinfo.html", locals())

            only = UserProfile.objects.filter(username=user.username)
            # Judge whether the user exists
            if len(only) == 0:
                msg = "The user does not exist"
                return render(request, "buy_userinfo.html", locals())
            only = only[0]
            only.address = address
            only.save()
            msg = "Modified successfully"
            return redirect("/buy_userinfo")
        else:
            return render(request, "buy_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
    return render(request, "buy_userinfo.html", locals())


# The judgment of modifying the seller's password
def modify_sell_password(request):
    # Confirm user
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        # Judge form input
        if request.method == "POST":
            user = request.user
            datas = request.POST
            # Extract form input
            old_password = request.POST.get("old_password")
            pwd1 = request.POST.get("pwd1")
            pwd2 = request.POST.get("pwd2")
            # Show incoming data
            # print("===")
            # print(old_password)
            # print(pwd1)
            # print(pwd2)

            # Judge whether the length of the old password and the new password meet the requirements
            if len(old_password) < 6 or len(pwd1) < 6 or len(pwd2) < 6:
                msg = "The password must be greater than 6 digits"
                return render(request, "sell_userinfo.html", locals())
            # Judge whether the new password entered twice is the same
            if pwd1 != pwd2:
                msg = "The two passwords are inconsistent"
                return render(request, "sell_userinfo.html", locals())

            # Judge whether the user exists according to the user name
            only = UserProfile.objects.filter(username=user.username)
            # Judge whether the user exists according
            if len(only) == 0:
                msg = "The user does not exist"
                return render(request, "sell_userinfo.html", locals())
            only = only[0]
            # # Show incoming data
            # print(only.password)
            # print(make_password(old_password))
            # print(only.password == make_password(old_password))

            # Determine whether the old password is entered correctly
            if check_password(old_password, only.password) == False:
                msg = "The old password is incorrect"
                return render(request, "sell_userinfo.html", locals())

            # Change the new password to the database
            only.password = make_password(pwd1)
            only.save()
            msg = "Modified successfully"
            # return seller information page
            return redirect("/sell_userinfo")
        else:
            msg = "Request error"
            # return seller information page
            return render(request, "sell_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        # return seller information page
        return render(request, "sell_userinfo.html", locals())


# Modify bank card number
def bank(request):
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        if request.method == "POST":
            user = request.user
            datas = request.POST
            bank_no = request.POST.get("bank_no")
            # The number of digits of a bank card number must be 16
            if len(bank_no) != 16:
                msg = "Bank card number must be 16 digits"
                return render(request, "sell_userinfo.html", locals())
            # Judge whether the user exists
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user does not exist"
                return render(request, "sell_userinfo.html", locals())
            only = only[0]
            only.bank_no = bank_no
            only.save()
            msg = "Modified successfully"
            return redirect("/sell_userinfo")
        else:
            return render(request, "sell_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
    return render(request, "sell_userinfo.html", locals())


# The buyer enters the amount to recharge into his account balance
def charging(request):
    user = request.user
    categories = Category.objects.filter()
    products = BuyPrice.objects.filter(user=user).values("product")
    orders = Order.objects.filter(user=user)
    try:
        if request.method == "POST":
            user = request.user
            datas = request.POST
            money = request.POST.get("money")
            # Determine that the input numbers conform to the correct format
            if "." in money:
                last = money.split(".")[1]
                if len(last) > 2:
                    msg = "Failure: decimal point must be followed by two digits!!!!!"
                    return render(request, "buy_userinfo.html", locals())
            # Verify that the input cannot be empty
            try:
                money = float(money)
            except Exception as e:
                print(e)
                msg = "Error: input is not a number or input cannot be empty!"
                return render(request, "buy_userinfo.html", locals())
            # Verify that the input cannot be equal to 0
            if money == 0.0:
                msg = "Error: recharge amount must be greater than 0"
                return render(request, "buy_userinfo.html", locals())
            # Judge whether the user exists
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user no longer exists"
                return render(request, "buy_userinfo.html", locals())
            only = only[0]
            # Input the amount plus the balance into the database
            only.money = only.money + money
            only.save()
            msg = "Recharge success"
            # return HttpResponse("Successful")
            # return redirect("/buy_userinfo")
            return render(request, "buy_userinfo.html", locals())
        else:
            msg = "Request error"
            # return HttpResponse("error")
            return render(request, "buy_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        return render(request, "buy_userinfo.html", locals())


# The balance of the seller's user is withdrawn from the required money to the user's bank card
def withdraw(request):
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        if request.method == "POST":
            user = request.user
            datas = request.POST
            money = request.POST.get("money")
            email = request.POST.get("email")
            bank_no = request.POST.get("bank_no")
            # Determine that the input money meets the requirements, and give a hint if it does not
            # Judge whether the input meets the currency standard
            if "." in money:
                last = money.split(".")[1]
                if len(last) > 2:
                    msg = "Failure: decimal point must be followed by two digits!!!!!"
                    return render(request, "buy_userinfo.html", locals())
            # Determines whether the input is empty or numeric
            try:
                money = float(money)
            except Exception as e:
                print(e)
                msg = "Error: input is not a number or input cannot be empty!"
                return render(request, "sell_userinfo.html", locals())
            # Determine that the input must be greater than 0
            if money == 0.0:
                msg = "Error: withdrawal amount must be greater than 0"
                return render(request, "sell_userinfo.html", locals())
            # Judge that the amount withdrawn by the user must be greater than the balance
            if int(money) > int(user.money):
                msg = "Error: the withdrawal amount must be less than the amount you have"
                return render(request, "sell_userinfo.html", locals())
            # Judge whether the user exists
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user does not exist"
                return render(request, "sell_userinfo.html", locals())
            only = only[0]
            # Save the balance minus the withdrawal amount into the database
            only.money = only.money - money
            only.save()
            msg = "Successful withdrawal"
            return redirect("/sell_userinfo")
        else:
            msg = "Request error"
            return render(request, "errinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        return render(request, "errinfo.html", locals())


# Re judgment of buyer user's modified information
def user_buy_modify(request):
    user = request.user
    categories = Category.objects.filter()
    products = BuyPrice.objects.filter(user=user).values("product")
    orders = Order.objects.filter(user=user)
    try:
        if request.method == "POST":
            user = request.user
            datas = request.POST
            username = request.POST.get("username")
            email = request.POST.get("email")
            address = request.POST.get("address")
            if len(username) < 6 or len(address) < 6:
                msg = "Username or address must be greater than 6 digits"
                return render(request, "buy_userinfo.html", locals())
            # Judge whether the user exists
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user no longer exists"
                return render(request, "buy_userinfo.html", locals())
            only = only[0]
            only.username = username
            only.email = email
            only.address = address
            only.save()
            msg = "Modified successfully"
            return redirect("/buy_userinfo")
        else:
            msg = "Request error"
            return render(request, "errinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        return render(request, "errinfo.html", locals())


# Re judgment of seller user after modifying information
def user_sell_modify(request):
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        if request.method == "POST":
            user = request.user
            datas = request.POST
            username = request.POST.get("username")
            email = request.POST.get("email")
            bank_no = request.POST.get("bank_no")
            if len(username) < 6 or re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,19}.com', email) == None or len(
                    bank_no) < 6:
                msg = "The user does not exist or have error"
                return render(request, "sell_userinfo.html", locals())
            # Judge whether the user exists
            only = UserProfile.objects.filter(username=user.username)
            if len(only) == 0:
                msg = "The user does not exist"
                return render(request, "sell_userinfo.html", locals())
            only = only[0]
            only.username = username
            only.email = email
            only.bank_no = bank_no
            only.save()
            msg = "Modified successfully"
            return redirect("/sell_userinfo")
        else:
            msg = "Request error"
            return render(request, "errinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System error"
        return render(request, "errinfo.html", locals())
