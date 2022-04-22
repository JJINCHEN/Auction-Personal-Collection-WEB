from .models import Product, Category, BuyPrice, Order, TransferMoney
from accounts.models import UserProfile
from .utils import *


def order_task():
    admin_user = UserProfile.objects.filter(username="JINCHEN")
    # print(admin_user)
    if len(admin_user) == 0:
        return False
    admin_user = admin_user[0]
    now = get_now_stamp()
    products = Product.objects.filter(sell_end_stamp__lte=now, status="4")
    # print("=====")
    print(products)
    for product in products:
        # print("Start Processing")
        # print(product)
        buy_price = BuyPrice.objects.filter(product=product)
        # print(buy_price)

        # Use price to judge whether the product is sold or not
        if len(buy_price) > 0:
            buy = buy_price.latest()
            first = buy_price[0].price
            for b in buy_price:
                if b.price > first:
                    buy = b
            # print(11111)
            # Modify the product status to "auction end"
            product.status = "5"
            product.buy_user = buy.user
            # print(buy.user)

            # Form an order
            order = Order()
            order.user = buy.user
            order.product = buy.product
            order.buy_price = buy
            order.price = buy.price
            order.save()
            product.save()
        else:
            # print("11")
            # print(product.price)
            # The company pays 10% compensation for not selling
            pei = product.price * 0.1
            # print(pei)
            product.status = "5"
            product.buy_user = admin_user

            # Form a transfer record
            transfer = TransferMoney()
            transfer.from_user = admin_user
            transfer.to_user = product.sell_user
            transfer.money = pei
            transfer.ttype = 2
            transfer.ptype = 1

            # The compensation money is deposited in the user's balance
            product.sell_user.money = product.sell_user.money + pei
            product.save()
            transfer.save()
            product.sell_user.save()
