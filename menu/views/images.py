from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from menu.errors import ItemDoesntExits, AddonDoesntExits
from menu.models import MenuItem, MenuAddon
from menu.serializers import (
    MenuItemImageSerializer,
    MenuAddonImageSerializer,
)


@permission_classes([IsAuthenticated])
class UploadMenuItemImage(APIView):
    def patch(self, request, item_id):
        try:
            menu_item = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            raise ItemDoesntExits
        serialized_data = MenuItemImageSerializer(instance=menu_item, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return JsonResponse(serialized_data.data, safe=False)


@permission_classes([IsAuthenticated])
class UploadMenuAddonImage(APIView):
    def patch(self, request, addon_id):
        try:
            menu_addon = MenuAddon.objects.get(id=addon_id)
        except MenuAddon.DoesNotExist:
            raise AddonDoesntExits
        serialized_data = MenuAddonImageSerializer(
            instance=menu_addon, data=request.data
        )
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return JsonResponse(serialized_data.data, safe=False)
