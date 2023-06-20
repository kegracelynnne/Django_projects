from django.contrib import admin

from pets.models import Type, Pet

# Register your models here.

admin.site.register(Type)
admin.site.register(Pet)