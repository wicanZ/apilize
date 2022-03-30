from django.contrib import admin

from .models import User   ,UserProfile ,TypesBikes ,Accessories ,BikeDetails
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
# admin.site.register(UserManager)
admin.site.register( TypesBikes )

admin.site.register( Accessories )

admin.site.register( BikeDetails )
