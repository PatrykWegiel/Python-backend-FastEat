import json

from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.errors import MenuDoesntExits, MenuAlreadyExits
from menu.models import Menu
from menu.serializers import (
    MenuSerializer,
)
from menu.views.base import BaseVenueView
from venue.models import Venue


class MenuView(BaseVenueView):
    @staticmethod
    def create(venue: Venue, data: dict) -> Menu:
        menu_serializer = MenuSerializer(data=data)
        menu_serializer.is_valid(raise_exception=True)
        menu = menu_serializer.save()
        venue.menu = menu
        venue.save(update_fields=["menu"])
        return menu

    @staticmethod
    def update(venue: Venue, data: dict) -> Menu:
        menu_serializer = MenuSerializer(venue.menu, data=data)

        menu_serializer.is_valid(raise_exception=True)
        menu = menu_serializer.save()
        return menu

    def get(self, request):
        menu = self.get_menu(self.request.user.pk)
        return Response(data=self.get_menu_json(menu), status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        venue = self.get_venue(self.request.user.pk)
        if venue.menu is not None:
            raise MenuAlreadyExits

        menu = self.create(venue, request.data)
        return Response(data=self.get_menu_json(menu), status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        menu = self.get_menu(self.request.user.pk)
        menu.delete()

        return Response(status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        venue = self.get_venue(self.request.user.pk)
        if venue.menu is None:
            raise MenuDoesntExits

        new_menu = self.update(venue, request.data)
        return Response(
            data=self.get_menu_json(new_menu), status=status.HTTP_201_CREATED
        )


@permission_classes([AllowAny])
class MenuPublicView(APIView):
    @staticmethod
    def _get_menu(pk) -> Menu:
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise MenuDoesntExits

    def get(self, request, menu_id):
        menu = self._get_menu(menu_id)
        menu_serializer = MenuSerializer(menu)
        menu_data = menu_serializer.data
        json_menu_data = json.loads(json.dumps(menu_data))
        return JsonResponse(json_menu_data)
