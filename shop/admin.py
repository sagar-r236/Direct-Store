from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Vendor)
admin.site.register(ProductCategory)
admin.site.register(Product)
