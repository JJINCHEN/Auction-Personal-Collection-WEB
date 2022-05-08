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
# Update information
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

# Statistics page Jump
@login_required
def statistics_index(request):
    user = request.user
    try:
        pass
    except Exception as e:
        print(e)
    return render(request, "statistics_index.html", locals())

# Boss page of the statistics information
@login_required
def statistics(request):
    user = request.user
    try:
        # Judge whether the user is boss or administrator
        if user.mtype != 2:
            msg = "You are not the BOSS can not view"
            return render(request, "errinfo.html", locals())

        # Count the number of different types of users
        buyer = UserProfile.objects.filter(mtype=0).count()
        seller = UserProfile.objects.filter(mtype=1).count()
        admin = UserProfile.objects.filter(mtype=2).count()
        total = TransferMoney.objects.filter().aggregate(money_total=Sum('money'))
        # print(total)
    except Exception as e:
        print(e)
    return render(request, "statistics.html", locals())

# Jump to monthly statistics page
@login_required
def monthly_statistics(request):
    user = request.user
    try:
        if user.mtype != 2:
            msg = "You are not the BOSS can not view"
            return render(request, "errinfo.html", locals())

    except Exception as e:
        print(e)
    return render(request, "monthly_statistics.html", locals())

# Statistics of expenditure information
@csrf_exempt
def expend_statistics(request):
    admin_user = UserProfile.objects.filter(username="JINCHEN")[0]
    x = []
    y = []
    # Choose a month from today as the starting time
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    # print(end_date, 'end_dates')

    # Time format conversion
    now_time = int(time.time()) + 86400
    day_time = now_time - now_time % 86400 + time.timezone
    dateArray = datetime.datetime.fromtimestamp(day_time)
    otherStyleTime = dateArray.strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d")

    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    # Time format conversion
    date_list.append("2022-05-25 00:00:00")
    date_list.append("2021-05-25 00:00:00")
    for i in range(len(date_list) - 1):
        begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")

        days = TransferMoney.objects.filter(to_user=admin_user, create_time__range=(begin, end))
        total = 0.0
        for day in days:
            total = total + float(day.money)
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(round(total, 2))
    yDict = {"name": "Daily expend", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["Daily expend"]
    }
    return success(last)

# Extraction of profit information
@csrf_exempt
def profit_statistics(request):
    admin_user = UserProfile.objects.filter(username="JINCHEN")[0]
    x = []
    y = []
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")

    # Time format conversion
    now_time = int(time.time()) + 86400
    day_time = now_time - now_time % 86400 + time.timezone
    dateArray = datetime.datetime.fromtimestamp(day_time)
    otherStyleTime = dateArray.strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    # Time format conversion
    date_list.append("2022-05-25 00:00:00")
    date_list.append("2022-05-25 00:00:00")
    for i in range(len(date_list) - 1):
        begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")

        income_days = TransferMoney.objects.filter(create_time__range=(begin, end), to_user=admin_user)
        income_total = 0.0
        for day in income_days:
            income_total = income_total + float(day.money)

        expend_days = TransferMoney.objects.filter(create_time__range=(begin, end), from_user=admin_user)
        expend_total = 0.0
        for day in expend_days:
            expend_total = expend_total + float(day.money)

        dif = income_total - expend_total
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(round(dif, 2))

    yDict = {"name": "Daily Profit", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["Daily Profit"]
    }
    return success(last)

# Information extraction and processing of daily statistics as website
@csrf_exempt
def day_statistics(request):
    x = []
    y = []
    # Calculate daily statistics within one month
    # Extract the time range of one month from now
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    # Time format conversion
    now_time = int(time.time()) + 86400
    day_time = now_time - now_time % 86400 + time.timezone
    dateArray = datetime.datetime.fromtimestamp(day_time)
    otherStyleTime = dateArray.strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    # Time format conversion
    date_list.append("2022-05-25 00:00:00")
    date_list.append("2022-05-25 00:00:00")
    for i in range(len(date_list) - 1):
        begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")

        days = TransferMoney.objects.filter(create_time__range=(begin, end))
        total = 0.0
        for day in days:
            total = total + float(day.money)
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(round(total, 2))
    yDict = {"name": "Platform turnover", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["Platform turnover"]
    }
    return success(last)


# Display statistics of a year by month
@csrf_exempt
def annual_statistics(request):
    x = []
    y = []
    # Gets the time one year before the current time, the earliest date is December 11, 2020
    begin_date = datetime.datetime.now().strftime("2020-12-11")
    # print(begin_date)
    date_list = getBetweenMonth(begin_date)
    date_list.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_list.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # print(date_list)
    for i in range(len(date_list) - 1):
        begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")

        days = TransferMoney.objects.filter(create_time__range=(begin, end))
        total = 0.0
        # Calculate monthly statistics
        for day in days:
            total = total + float(day.money)
        # Select the value of the XY coordinate
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(round(total, 2))
    yDict = {"name": "Monthly System Statement", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["Monthly System Statement"]
    }
    return success(last)


# Display statistics by selected time period
@login_required
def search_data(request):
    user = request.user
    try:
        # Judge whether the user is boss or administrator
        if user.mtype != 2:
            msg = "You are not the BOSS can not view"
            return render(request, "errinfo.html", locals())

        keywords = request.GET.get('keywords', '')
        try:
            keywords = keywords.strip()
        except:
            pass
        if keywords is None or keywords == "":
            expenditure_statistics = TransferMoney.objects.filter(from_user_id=1).aggregate(money_total=Sum('money'))
            income_statistics = TransferMoney.objects.filter(to_user_id=1).aggregate(money_total=Sum('money'))
            turnover_statistics = TransferMoney.objects.filter(~Q(from_user_id=1), ~Q(to_user_id=1)).aggregate(
                money_total=Sum('money'))
        else:
            date_arr = keywords.split(" - ")
            start_date = date_arr[0] + " 00:00:00"
            end_date = date_arr[1] + " 23:59:59"
            expenditure_statistics = TransferMoney.objects.filter(create_time__gte=start_date, create_time__lte=end_date).filter(
                from_user_id=1).aggregate(money_total=Sum('money'))
            income_statistics = TransferMoney.objects.filter(create_time__gte=start_date, create_time__lte=end_date).filter(
                to_user_id=1).aggregate(money_total=Sum('money'))
            turnover_statistics = TransferMoney.objects.filter(create_time__gte=start_date,
                                                          create_time__lte=end_date).filter(~Q(from_user_id=1),
                                                                                            ~Q(to_user_id=1)).aggregate(
                money_total=Sum('money'))
    except Exception as e:
        print(e)
    return render(request, "search_data.html", locals())


# Method of taking month range
def getBetweenMonth(begin_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    # print(begin_date)
    # print(end_date)
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-01 %H:%M:%S")
        date_list.append(date_str)
        begin_date = add_months(begin_date, 1)
    return date_list

def add_months(dt, months):
    month = dt.month - 1 + months
    # print(month)
    year = int(dt.year + month / 12)
    # print(year)
    month = int(month % 12) + 1
    # print(month)
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

def menu(request):
    try:
        user = request.user
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(settings.MENU))


# Seller personal information page Jump
@login_required
def sell_userinfo(request):
    user = request.user
    users = UserProfile.objects.filter()
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
                # print(begin)
                # print(end)
                begin_mysql = datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
                end_mysql = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                begin_stamp = get_stamp_by_time(begin)
                end_stamp = get_stamp_by_time(end)
                # print(end_stamp)
                # print(begin_stamp)
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
            # print(cid)
            category_obj = Category.objects.filter(id=cid)
            # print(category_obj)
            if len(category_obj) > 0:
                category_obj = category_obj[0]
                all_products = all_products.filter(category=category_obj)
        # Display by search
        if search:
            all_products = all_products.filter(name__contains=search, detail=search)
        # Search all product names with search data
        for product in all_products:
            # print(product.name)
            now = float(get_now_stamp())
            begin = product.sell_begin_stamp
            end = product.sell_end_stamp
            dif = begin - now
            if now < begin:
                product.__setattr__("mstatus", "0")
                product.__setattr__("dif", str(int(dif)))
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
    # print(user.mtype)
    try:
        # It is necessary to judge that the bidding user is the buyer
        if request.method == "POST" and user.mtype == 0:
            # print(request.POST)
            # print(request.body)
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
            # print(request.POST)
            # print(request.body)
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
