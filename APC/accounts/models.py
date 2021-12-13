from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    # Set user role type id
    STATUS_CHOICES = (
        (0, 'Buyer'),
        (1, 'Seller'),
        (2, 'Administrator'),
    )

    mtype = models.IntegerField(verbose_name='user_type', blank=True, null=True, default=0, choices=STATUS_CHOICES)
    address = models.CharField(verbose_name='user_address', blank=True, null=True, default="", max_length=500)
    bank_no = models.CharField(verbose_name='user_address', blank=True, null=True, default="", max_length=500)
    money = models.FloatField(verbose_name='Balance', blank=True, null=True, default=0.0)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        verbose_name = 'User management'
        verbose_name_plural = verbose_name
