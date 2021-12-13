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
]
