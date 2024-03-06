from django.contrib import admin
from menu.models import Menu, MenuCategory, MenuItem, MenuAddon

admin.site.register(Menu)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(MenuAddon)
