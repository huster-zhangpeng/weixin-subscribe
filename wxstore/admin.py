from django.contrib import admin
from wxstore.models import Store, Good, Order, Buy, Address, Rate

admin.site.register(Store)
admin.site.register(Good)
admin.site.register(Order)
admin.site.register(Buy)
admin.site.register(Address)
admin.site.register(Rate)
