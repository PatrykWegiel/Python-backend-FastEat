from django.urls import path

from menu.views.addon import AddonView
from menu.views.category import CategoryView
from menu.views.item import ItemView
from menu.views.menu import MenuView, MenuPublicView
from menu.views.images import (
    UploadMenuAddonImage,
    UploadMenuItemImage,
)

urlpatterns = [
    path("menu/", MenuView.as_view()),
    path("categories/", CategoryView.as_view()),
    path("categories/<int:category_id>", CategoryView.as_view()),
    path("categories/<int:category_id>/item", ItemView.as_view()),
    path("items/<int:item_id>", ItemView.as_view()),
    path("items/<int:item_id>/image", UploadMenuItemImage.as_view()),
    path("items/<int:item_id>/addon", AddonView.as_view()),
    path("addons/<int:addon_id>", AddonView.as_view()),
    path("addons/<int:addon_id>/image", UploadMenuAddonImage.as_view()),
    path("menu-public/<int:menu_id>", MenuPublicView.as_view()),
]
