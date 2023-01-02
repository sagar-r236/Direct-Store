from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, default='whatever')
    mobile_number = models.IntegerField(primary_key=True)
    user_pincode = models.IntegerField()
    user_latitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    user_longitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    otp = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name + str(self.mobile_number)


