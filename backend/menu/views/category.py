from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from menu.errors import CategoryDoesntExits
from menu.models import Menu, MenuCategory
from menu.serializers import (
    CategorySerializer,
)
from menu.views.base import BaseVenueView


@permission_classes([IsAuthenticated])
class CategoryView(BaseVenueView):
    @staticmethod
    def create(menu: Menu, data: dict) -> Menu:
        category_serializer = CategorySerializer(data=data)
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()
        category.menu = menu
        category.save(update_fields=["menu"])
        return menu

    @staticmethod
    def update(category: MenuCategory, data: dict) -> Menu:
        category_serializer = CategorySerializer(category, data=data)
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()
        return category.menu

    @staticmethod
    def _get_category(category_id, menu) -> MenuCategory:
        if category_id is None:
            raise CategoryDoesntExits
        try:
            return MenuCategory.objects.get(menu=menu, id=category_id)
        except MenuCategory.DoesNotExist:
            raise CategoryDoesntExits

    def post(self, request, category_id=None):
        menu = self.get_menu(self.request.user.pk)
        updated_menu = self.create(menu, request.data)
        return Response(
            data=self.get_menu_json(updated_menu), status=status.HTTP_201_CREATED
        )

    def delete(self, request, category_id=None):
        menu = self.get_menu(self.request.user.pk)
        category = self._get_category(category_id, menu)
        category.delete()

        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)

    def patch(self, request, category_id=None):
        menu = self.get_menu(self.request.user.pk)

        category = self._get_category(category_id, menu)
        new_menu = self.update(category, request.data)

        return Response(
            data=self.get_menu_json(new_menu), status=status.HTTP_201_CREATED
        )
