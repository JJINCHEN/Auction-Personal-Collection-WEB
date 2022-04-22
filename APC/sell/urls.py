from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r"detail_products", detail_products, name="detail_products"),
    url(r"products", products, name="products"),

    url(r"buy_userinfo", buy_userinfo, name="buy_userinfo"),
    url(r"sell_userinfo", sell_userinfo, name="sell_userinfo"),
    url(r"add_pro", add_pro, name="add_pro"),

    url(r"bid", bid, name="bid"),
    url(r"pay", pay, name="pay"),
    url(r"contract", contract, name="contract"),
    url(r"^$", index, name="index"),
]
