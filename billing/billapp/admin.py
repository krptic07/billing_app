from django.contrib import admin
from billapp.models import bill,UserProfileInfo

# Register your models here.

admin.site.register(bill)
admin.site.register(UserProfileInfo)
