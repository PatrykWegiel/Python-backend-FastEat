from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from menu.errors import ItemDoesntExits, AddonDoesntExits
from menu.models import Menu, MenuItem, MenuAddon
from menu.serializers import (
    MenuAddonSerializer,
)
from menu.views.base import BaseVenueView


@permission_classes([IsAuthenticated])
class AddonView(BaseVenueView):
    @staticmethod
    def _get_addon(addon_id, menu) -> MenuAddon:
        if addon_id is None:
            raise AddonDoesntExits
        try:
            return MenuAddon.objects.get(
                pk=addon_id,
                item__category__menu_id=menu.pk,
            )
        except MenuAddon.DoesNotExist:
            raise AddonDoesntExits

    @staticmethod
    def _get_item(item_id, menu) -> MenuItem:
        if item_id is None:
            raise ItemDoesntExits
        try:
            return MenuItem.objects.get(category__menu=menu, id=item_id)
        except MenuItem.DoesNotExist:
            raise ItemDoesntExits

    @staticmethod
    def create(item: MenuItem, data: dict) -> Menu:
        addon_serializer = MenuAddonSerializer(data=data)
        addon_serializer.is_valid(raise_exception=True)
        addon = addon_serializer.save()
        addon.item = item
        addon.save(update_fields=["item"])
        return addon.item.category.menu

    @staticmethod
    def update(addon: MenuAddon, data: dict) -> Menu:
        addon_serializer = MenuAddonSerializer(addon, data=data)

        addon_serializer.is_valid(raise_exception=True)
        addon = addon_serializer.save()
        return addon.item.category.menu

    def post(self, request, item_id=None, addon_id=None):
        menu = self.get_menu(self.request.user.pk)
        item = self._get_item(item_id, menu)
        self.create(item, request.data)

        return Response(data=self.get_menu_json(menu), status=status.HTTP_201_CREATED)

    def delete(self, request, item_id=None, addon_id=None):
        menu = self.get_menu(self.request.user.pk)
        addon = self._get_addon(addon_id, menu)
        addon.delete()

        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)

    def patch(self, request, addon_id=None, item_id=None):
        menu = self.get_menu(self.request.user.pk)
        addon = self._get_addon(addon_id, menu)
        self.update(addon, request.data)

        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)
