from django.db import models
from accounts.models import UserProfile


# Create your models here.

# Product category
class Category(models.Model):
    name = models.CharField(verbose_name='Product category', default='', max_length=500)

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product category'

    def __str__(self):
        return self.name


# Product status
class Product(models.Model):
    STATUS_CHOICES = (
        ('0', 'Check pending'),
        ('1', 'Pass the check'),
        ('2', 'Unapproved'),
        ('3', 'Unidentified'),
        ('4', 'Pass identified'),
        ('5', 'Auction over'),
    )

    name = models.CharField(verbose_name='Product name', default='', max_length=500)
    img = models.ImageField(upload_to='img/', verbose_name='Product image', blank=True, default='', max_length=500)
    detail = models.CharField(verbose_name='Product details', default='', max_length=1000)
    sell_user = models.ForeignKey(UserProfile, verbose_name="Seller", on_delete=models.CASCADE,
                                  related_name="sellers")
    buy_user = models.ForeignKey(UserProfile, verbose_name="Buyer", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="buyers")
    sell_begin = models.DateTimeField(verbose_name='Auction Start Date')
    sell_begin_stamp = models.FloatField(verbose_name='Auction start date time stamp seconds', default=0)
    sell_end = models.DateTimeField(verbose_name='Auction End Date')
    sell_end_stamp = models.FloatField(verbose_name='Auction end date time stamp seconds', default=0)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    price = models.FloatField(default=0.0, verbose_name="Prices")
    status = models.CharField(default="0", verbose_name="Status", choices=STATUS_CHOICES, max_length=2)
    updated = models.DateTimeField(auto_now=True, verbose_name='Modification time')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Creat time')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name

    def get_current_price(self):
        price = self.price
        user_buy = BuyPrice.objects.filter(product=self)
        if len(user_buy) > 0:
            latest = user_buy.latest()
            price = latest.price
        return price

    def get_current_user(self):
        # print(1111111)
        user = "No one bought it"
        user_buy = BuyPrice.objects.filter(product=self)
        if len(user_buy) > 0:
            latest = user_buy.latest()
            user = latest.user.username
        return user


class BuyPrice(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="Buyer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    price = models.FloatField(default=0.0, verbose_name="Prices")
    updated = models.DateTimeField(auto_now=True, verbose_name='Modification time')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Creat time')

    class Meta:
        verbose_name = 'Buyer bid'
        verbose_name_plural = 'Buyer bid'
        get_latest_by = 'updated'

    def __str__(self):
        return self.user.username


# Order status
class Order(models.Model):
    STATUS_CHOICES = (
        ('0', 'Auction closed, unpaid'),
        ('1', 'Paid'),
        ('2', 'Undelivered'),
        ('3', 'Delivered'),
        ('4', 'Complete'),
    )
    user = models.ForeignKey(UserProfile, verbose_name="Buyer", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    buy_price = models.ForeignKey(BuyPrice, verbose_name="Purchase history", on_delete=models.CASCADE)
    price = models.FloatField(default=0.0, verbose_name="Prices")
    status = models.CharField(default="0", verbose_name="Status", choices=STATUS_CHOICES, max_length=2)
    updated = models.DateTimeField(auto_now=True, verbose_name='Modification time')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Creat time')

    class Meta:
        verbose_name = 'Order Information'
        verbose_name_plural = 'Order Information'
        get_latest_by = 'updated'

    def __str__(self):
        return self.user.username


class TransferMoney(models.Model):
    TTYPE_CHOICES = (
        (1, 'Buy transfer'),
        (2, 'Not sold, company expense'),
    )

    from_user = models.ForeignKey(UserProfile, verbose_name="From the user", related_name="money_from_user",
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, verbose_name="Transfer in user", related_name="money_to_user",
                                on_delete=models.CASCADE)
    money = models.FloatField(verbose_name='Number', default=0.0)
    update_time = models.DateTimeField(auto_now=True, verbose_name='Modification time')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
    ttype = models.IntegerField(default=1, verbose_name="Transfer Type", choices=TTYPE_CHOICES)

    def __str__(self):
        return str(self.from_user)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Money transfer information'
        verbose_name_plural = verbose_name
