from django.contrib import admin
from .models import User,Customer,Admin,Application,Level
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Application)
admin.site.register(Level)