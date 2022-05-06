from django.urls import path
from .views import *

urlpatterns = [
    # Routing path: Jump page according to route
    path(r"login/", user_login, name="login"),
    path(r"logout/", user_logout, name="logout"),
    path(r"do_sell_register/", do_sell_register, name="register"),
    path(r"do_buy_register/", do_buy_register, name="register"),
    path(r"buy_register/", buy_register, name="buy_register"),
    path(r"sell_register/", sell_register, name="sell_register"),

    path(r"modify_buy_password", modify_buy_password, name="modify_buy_password"),
    path(r"address", address, name="address"),
    path(r"charging", charging, name="charging"),
    path(r"user_buy_modify", user_buy_modify, name="user_buy_modify"),

    path(r"modify_sell_password", modify_sell_password, name="modify_sell_password"),
    path(r"bank", bank, name="bank"),
    path(r"withdraw", withdraw, name="withdraw"),
    path(r"user_sell_modify", user_sell_modify, name="user_sell_modify"),
]
