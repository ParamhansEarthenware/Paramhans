from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(Order)
admin.site.register(DeliveredOrder)