from django.contrib import admin
from . models import csv_data
from . models import temp_ssdata
# Register your models here.

admin.site.register(csv_data)
admin.site.register(temp_ssdata)