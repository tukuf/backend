from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Land)
admin.site.register(Inquiry)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(Notification)
