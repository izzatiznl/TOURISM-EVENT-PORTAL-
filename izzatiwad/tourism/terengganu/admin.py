from django.contrib import admin
from terengganu.models import Customer ,Package,Booking, Review
# Register your models here.

admin.site.register(Customer)
admin.site.register(Package)
admin.site.register(Review)
admin.site.register(Booking)