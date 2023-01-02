from django.db import models

# Create your models here.


class Vendor(models.Model):
    shop_name = models.TextField(max_length=50)
    mobile_number = models.CharField(max_length=10, primary_key=True)
    password = models.TextField(max_length=50)
    pincode = models.IntegerField()
    otp = models.IntegerField(null=True, default=None, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.shop_name