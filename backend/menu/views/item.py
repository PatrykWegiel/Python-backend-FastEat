from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from menu.errors import CategoryDoesntExits, ItemDoesntExits
from menu.models import Menu, MenuCategory, MenuItem
from menu.serializers import MenuItemSerializer
from menu.views.base import BaseVenueView


@permission_classes([IsAuthenticated])
class ItemView(BaseVenueView):
    @staticmethod
    def _get_item(item_id, menu) -> MenuItem:
        if item_id is None:
            raise ItemDoesntExits
        try:
            return MenuItem.objects.get(category__menu=menu, id=item_id)
        except MenuItem.DoesNotExist:
            raise ItemDoesntExits

    @staticmethod
    def _get_category(category_id, menu) -> MenuCategory:
        if category_id is None:
            raise CategoryDoesntExits
        try:
            return MenuCategory.objects.get(menu=menu, id=category_id)
        except MenuCategory.DoesNotExist:
            raise CategoryDoesntExits

    @staticmethod
    def create(category: MenuCategory, data: dict) -> Menu:
        item_serializer = MenuItemSerializer(data=data)
        item_serializer.is_valid(raise_exception=True)
        item = item_serializer.save()
        item.category = category
        item.save(update_fields=["category"])
        return item.category.menu

    @staticmethod
    def update(item: MenuItem, data: dict) -> Menu:
        item_serializer = MenuItemSerializer(item, data=data)
        item_serializer.is_valid(raise_exception=True)
        item = item_serializer.save()
        return item.category.menu

    def post(self, request, category_id=None, item_id=None):
        menu = self.get_menu(self.request.user.pk)
        category = self._get_category(category_id, menu)
        new_menu = self.create(category, request.data)

        return Response(
            data=self.get_menu_json(new_menu), status=status.HTTP_201_CREATED
        )

    def delete(self, request, item_id=None, category_id=None):
        menu = self.get_menu(self.request.user.pk)
        item = self._get_item(item_id, menu)
        item.delete()

        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)

    def patch(self, request, item_id=None, category_id=None):
        menu = self.get_menu(self.request.user.pk)
        item = self._get_item(item_id, menu)
        self.update(item, request.data)

        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)
