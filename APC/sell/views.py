from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, BuyPrice, Order, TransferMoney
from accounts.models import UserProfile
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import time
from django.db.models import Max, Q
import os
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from .task import order_task
import json
from django.db.models import Count, Sum
import datetime
from .json_response import *
import calendar


# Create your views here.
# Jump to main page
def index(request):
    try:
        order_task()
    except Exception as e:
        print(e)
    return render(request, "index.html", locals())

# Jump to display contract page
def contract(request):
    try:
        pass
    except Exception as e:
        print(e)
    return render(request, "contract.html", locals())

# Seller personal information page Jump
@login_required
def sell_userinfo(request):
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        pass
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "errinfo.html", locals())
    return render(request, "sell_userinfo.html", locals())


# Buyer's personal information page Jump
@login_required
def buy_userinfo(request):
    user = request.user
    categories = Category.objects.filter()
    products = []
    cash = []
    orders = Order.objects.filter(user=user)
    for buy in BuyPrice.objects.filter(user=user):
        if buy.product.id in cash:
            continue
        else:
            products.append(buy.product)
            cash.append(buy.product.id)
    # Show incoming data
    # print(products)
    # print(cash)
    # print("----")
    try:
        pass
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "errinfo.html", locals())
    return render(request, "buy_userinfo.html", locals())


# The seller user adds the product
@login_required
def add_pro(request):
    user = request.user
    categories = Category.objects.filter()
    products = Product.objects.filter(sell_user=user)
    try:
        if request.method == "POST":
            # If it is a POST request, get the submitted parameters
            image = request.FILES.get('img')
            name = request.POST.get("name")
            detail = request.POST.get("detail")
            price = request.POST.get("price")
            timerange = request.POST.get("timerange")
            category = request.POST.get("category")
            # Show incoming data
            # print("===============")
            # print(name)
            # print(detail)
            # print(price)
            # print(timerange)
            # print(category)
            if len(name) == 0 or len(timerange) == 0:
                msg = "The name or auction time cannot be empty"
                return render(request, "sell_userinfo.html", locals())
            if len(name) == 0:
                msg = "Name cannot be empty"
                return render(request, "sell_userinfo.html", locals())
            if len(detail) == 0:
                msg = "Product description cannot be empty"
                return render(request, "sell_userinfo.html", locals())
            if len(detail) < 5:
                msg = "Product description cannot be small than 5 characters"
                return render(request, "sell_userinfo.html", locals())
            try:
                price = float(price)
            except Exception as e:
                print(e)
                msg = "Error: The base price entered is not a number!"
                return render(request, "sell_userinfo.html", locals())
            try:
                time_split = timerange.split(" - ")
                begin = time_split[0]
                end = time_split[1]
                print(begin)
                print(end)
                begin_mysql = datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
                end_mysql = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                begin_stamp = get_stamp_by_time(begin)
                end_stamp = get_stamp_by_time(end)
                print(end_stamp)
                print(begin_stamp)
                if float(end_stamp) <= float(begin_stamp):
                    msg = "Error: End time is less than or equal to start time!"
                    return render(request, "sell_userinfo.html", locals())

            except Exception as e:
                print(e)
                msg = "Error: Incorrect time format!"
                return render(request, "sell_userinfo.html", locals())
            if image:
                # According to the picture information submitted by the front end, save the picture and get the name of the picture
                file_name = str(int(time.time())) + "." + image.name.split(".")[-1]
                path = os.path.join(settings.MEDIA_ROOT, "img")
                path = os.path.join(path, file_name)
                last_path = default_storage.save(path, ContentFile(image.read()))

            else:
                msg = "Error: Picture cannot be empty!"
                return render(request, "sell_userinfo.html", locals())
            category_obj = Category.objects.filter(id=category)
            if len(category_obj) == 0:
                msg = "Error: Classification no exists!"
                return render(request, "sell_userinfo.html", locals())
            category_obj = category_obj[0]
            # Add new product to database
            product = Product()
            product.sell_user = user
            product.name = name
            product.detail = detail
            product.img = "img/" + file_name
            product.sell_begin = begin_mysql
            product.sell_begin_stamp = float(begin_stamp)
            product.sell_end = end_mysql
            product.sell_end_stamp = float(end_stamp)
            product.category = category_obj
            product.price = float(price)
            product.save()
            msg = "Added successfully"
            return render(request, "sell_userinfo.html", locals())
    except Exception as e:
        print(e)
    return render(request, "sell_userinfo.html", locals())


# Display of product list (according to different conditions)
def products(request):
    try:
        # Get the categories in the navigation bar and search for information
        cid = request.GET.get("cid", "")
        search = request.GET.get("search", "")
        # Response code =4= the status of the approved item.
        all_products = Product.objects.filter(status="4")
        all_category = Category.objects.filter()
        # Display by category ID
        if cid:
            print(cid)
            category_obj = Category.objects.filter(id=cid)
            print(category_obj)
            if len(category_obj) > 0:
                category_obj = category_obj[0]
                all_products = all_products.filter(category=category_obj)
        # Display by search
        if search:
            all_products = all_products.filter(name__contains=search)
        # Search all product names with search data
        for product in all_products:
            print(product.name)
            now = float(get_now_stamp())
            begin = product.sell_begin_stamp
            end = product.sell_end_stamp
            dif = begin - now
            if now < begin:
                product.__setattr__("mstatus", "0")
                product.__setattr__("cha", str(int(dif)))
            elif now >= begin and now <= end:
                product.__setattr__("mstatus", "1")
            else:
                product.__setattr__("mstatus", "2")
            user_buy = BuyPrice.objects.filter(product=product)
            # Judge the current price of the product
            if len(user_buy) > 0:
                latest = user_buy.latest()
                product.price = latest.price
            # price = BuyPrice.objects.filter(product=product).aggregate(Max('price'))
            # if "price__max" in price and price["price"] != None:
            #     product.price = price
    except Exception as e:
        print(e)
    return render(request, "products.html", locals())


# Extract the product information and display the product details page
@login_required
def detail_products(request):
    try:
        pid = request.GET.get("pid", "")
        # Show incoming data
        # print(request.GET)
        # print(pid)
        product = Product.objects.filter(id=int(pid))
        if len(product) == 0:
            msg = "The products not exist"
            return render(request, "errinfo.html", locals())
        product = product[0]
        user_buy = BuyPrice.objects.filter(product=product)
        if len(user_buy) > 0:
            latest = user_buy.latest()
        else:
            latest = {}
        return render(request, "detail_products.html", locals())
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "errinfo.html", locals())


# Add bidding information
@login_required
@csrf_exempt
def bid(request):
    user = request.user
    print(user.mtype)
    try:
        # It is necessary to judge that the bidding user is the buyer
        if request.method == "POST" and user.mtype == 0:
            print(request.POST)
            print(request.body)
            # If it is a POST request, get the submitted parameters
            price = request.POST.get("price")
            pid = request.POST.get("pid")
            # Show incoming data
            # print("===============")
            # print(price)
            # print(pid)
            product = Product.objects.filter(id=int(pid))
            if len(product) > 0:
                product = product[0]
            else:
                msg = "Failure: The item does not exist"
                return HttpResponse("Failure: The item does not exist")
            if "." in price:
                last = price.split(".")[1]
                if len(last) > 2:
                    return HttpResponse("Failure: At most two decimal places!!!")
            try:
                # Amount conversion to number
                price = float(price)
            except Exception as e:
                print(e)
                return HttpResponse("Failure: Please enter the number")
            # If there are decimals in the input number, is it in accordance with the currency standard
            if price <= product.price:
                return HttpResponse("Failure: Can not be less than or equal to the base price of products")
            buy = BuyPrice.objects.filter(product=product)
            if len(buy) > 0:
                buy = buy.latest()
                if price <= buy.price:
                    return HttpResponse("Failed: Latest bid for‘" + str(buy.price) + "’. You must be above this price")
            now = float(get_now_stamp())
            # Show incoming data
            # print("========")
            # print(now)
            # print(product.sell_begin_stamp)
            # print(product.sell_end_stamp)
            if now < product.sell_begin_stamp or now > product.sell_end_stamp:
                return HttpResponse("Failure: Not within auction time")
            user_buy = BuyPrice()
            user_buy.user = user
            user_buy.product = product
            user_buy.price = price
            user_buy.save()
            return HttpResponse("Successful")
        else:
            msg = "System Error"
            return HttpResponse("Your identity is not allowed to bid")
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "errinfo.html", locals())


# Buyer to pay
@login_required
@csrf_exempt
def pay(request):
    user = request.user
    categories = Category.objects.filter()
    products = BuyPrice.objects.filter(user=user).values("product")
    orders = Order.objects.filter(user=user)
    try:
        if request.method == "POST":
            print(request.POST)
            print(request.body)
            # If it is a POST request, get the submitted parameters
            pid = request.POST.get("pid")
            order = Order.objects.filter(id=int(pid))
            if len(order) > 0:
                order = order[0]
            else:
                msg = "Failure: The products not exist"
                return HttpResponse("Failure: The order not exist")
            if order.user.money < order.price:
                return HttpResponse("Failed: Your balance is insufficient, please charging")
            admin_user = UserProfile.objects.filter(username="JINCHEN")[0]
            # Payment status changed to complete
            order.status = "1"
            order.save()
            # Modify account balance
            order.user.money = order.user.money - order.price
            order.user.save()

            # Money for the seller
            sell_money = order.price * 0.95
            # Money for the company
            admin_money = order.price * 0.05

            order.product.sell_user.money = order.product.sell_user.money + sell_money
            admin_user.money = admin_user.money + admin_money

            order.product.sell_user.save()
            admin_user.save()

            user_transfer = TransferMoney(
                from_user=order.user,
                to_user=order.product.sell_user,
                money=sell_money,
                ttype=2
            )

            user_admin = TransferMoney(
                from_user=order.user,
                to_user=admin_user,
                money=admin_money,
                ttype=2
            )
            user_transfer.save()
            user_admin.save()

            return HttpResponse("Successful")
        return render(request, "buy_userinfo.html", locals())
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "buy_userinfo.html", locals())
