from django.contrib import admin

# Register your models here.
from chef.models import *

admin.site.register(Blog)
admin.site.register(Chef)
admin.site.register(Course)