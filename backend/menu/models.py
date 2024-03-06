import os

from django.db import models
from django_resized import ResizedImageField


def menu_addon_image_upload(instance, filename):
    path = "menu/addon"
    file_extension = filename.split(".")[1]
    format = str(instance.id) + "_" + instance.name + "." + file_extension
    return os.path.join(path, format)

def menu_item_image_upload(instance, filename):
    path = "menu/item"
    file_extension = filename.split(".")[1]
    format = str(instance.id) + "_" + instance.name + "." + file_extension
    return os.path.join(path, format)


"""
A Menu represents a collection of categories of food items. For example,
a restaurant may have a Lunch menu, and a Dinner menu.
"""


class Menu(models.Model):
    name = models.CharField(max_length=24, verbose_name="menu name")
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Any additional text that the menu might need, i.e. Served between 11:00am and 4:00pm.",
    )

    def __str__(self):
        return f"{self.name}"


"""
A Menu Category represents a grouping of items within a specific Menu.
An example of a Menu Category would be Appetizers, or Pasta.
"""


class MenuCategory(models.Model):
    menu = models.ForeignKey(
        Menu,
        help_text="The menus that this category belongs to, i.e. 'Lunch'.",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=32, verbose_name="menu category name")
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="The additional text is any bit of related information to go along with a menu category, i.e. the 'Pasta' category might have details that say 'All entrees come with salad and bread'.",
    )
    sequence = models.IntegerField(
        default=0,
        help_text="The order is the order that this category should appear in when rendered on the templates.",
    )

    class Meta:
        verbose_name = "menu category"
        verbose_name_plural = "menu categories"
        ordering = ["sequence", "name"]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


"""
A Menu Item is an item of food that the restaurant makes. A Menu Item can
belong to one Menu.
"""


class MenuItem(models.Model):
    name = models.CharField(max_length=48, help_text="Name of the item on the menu.")
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="The description is a simple text description of the menu item.",
    )
    category = models.ForeignKey(
        MenuCategory,
        verbose_name="menu category",
        help_text="Category is the menu category that this menu item belongs to, i.e. 'Appetizers'.",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="items",
    )
    sequence = models.IntegerField(
        default=0,
        verbose_name="sequence",
        help_text="The order is to specify the order in which items show up on the menu.",
    )
    price = models.IntegerField(help_text="The price is the cost of the item.")
    image = ResizedImageField(
        size=[150, 150],
        upload_to=menu_item_image_upload,
        null=True,
        blank=True,
        force_format="PNG",
    )

    class Meta:
        verbose_name = "menu item"
        verbose_name_plural = "menu items"
        ordering = ["category", "sequence", "name"]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f"{self.name}"


"""
A Menu Item is an item of food that the restaurant makes. A Menu Item can
belong to multiple Menu Categories to facilitate menus that have the same item
across multiple menus.
"""


class MenuAddon(models.Model):
    name = models.CharField(max_length=48, help_text="Name of the item on the menu.")
    description = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="The description is a simple text description of the menu addon.",
    )
    item = models.ForeignKey(
        MenuItem,
        verbose_name="menu item",
        help_text="Addon is the Item category that this menu item belongs to, i.e. 'Appetizers'.",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="addons",
    )
    sequence = models.IntegerField(
        default=0,
        verbose_name="sequence",
        help_text="The order is to specify the order in which items show up on the menu.",
    )
    price = models.IntegerField(help_text="The price is the cost of the item.")
    image = ResizedImageField(
        size=[150, 150],
        upload_to=menu_addon_image_upload,
        null=True,
        blank=True,
        force_format="PNG",
    )

    class Meta:
        verbose_name = "menu addon"
        verbose_name_plural = "menu addons"
        ordering = ["item", "sequence", "name"]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f"{self.name}"
