import json
from abc import abstractmethod
from typing import Dict

from django.db import transaction, models
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
from menu.errors import VenueDoesntExits, MenuDoesntExits
from menu.models import Menu
from menu.serializers import (
    MenuSerializer,
)
from venue.models import Venue


@permission_classes([IsAuthenticated])
class BaseVenueView(APIView):
    @staticmethod
    def get_menu_json(menu: Menu) -> Dict[str, str]:
        """
        Parse menu to json

        :param menu: Menu model
        :return: Menu json
        """
        new_menu_serializer = MenuSerializer(menu)
        return json.loads(json.dumps(new_menu_serializer.data))

    @staticmethod
    def get_venue(user_id) -> Venue:
        """
        Get logged venue

        :param user_id: logged in user id
        :return: Venue obj
        """
        try:
            return Venue.objects.get(owner=user_id)
        except Venue.DoesNotExist:
            raise VenueDoesntExits

    def get_menu(self, user_id) -> Menu:
        """
        Get menu for logged user

        :param user_id: logged in user id
        :return: Menu obj
        """
        venue = self.get_venue(user_id)
        if venue.menu is None:
            raise MenuDoesntExits

        return venue.menu

    @staticmethod
    @abstractmethod
    def create(obj: models.Model, data: Dict[str, any]) -> Menu:
        """
        Reference to create model method

        :param obj: model to which we will be crated
        :param data: data to be added
        :return: the entire menu
        """

    @staticmethod
    @abstractmethod
    def update(obj: models.Model, data: Dict[str, any]) -> Menu:
        """
        Reference to update model method

        :param obj: model to which we will be updated
        :param data: data to be added
        :return: the entire menu
        """

    @abstractmethod
    def post(self, request, **kwargs):
        """
        Rest method to add obj

        :param request:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def delete(self, request, **kwargs):
        """
        Rest method to delete obj

        :param request:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def patch(self, request, **kwargs):
        """
        Rest method to edit obj

        :param request:
        :param kwargs:
        :return:
        """
