import json
from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .errors import (
    VenueDoesntExists,
    UserFavoriteVenueDoesntExist,
    UserFavoriteVenueAlreadyExists,
    RequiredImage,
)
from .serializers import *


@permission_classes([AllowAny])
class VenueList(ListAPIView):
    def get_queryset(self):
        """
        This view should return a list of all the venues in a city
        """
        self.serializer_class = (
            VenueListSerializer
            if self.request.user.is_anonymous
            else AuthVenueListSerializer
        )

        venues = Venue.objects.all()
        city = self.request.query_params.get("city")
        kitchen_type = self.request.query_params.get("kitchenType")
        free_delivery = self.request.query_params.get("freeDelivery")
        availability = self.request.query_params.get("availability")
        rating = self.request.query_params.get("rating")
        order_by = self.request.query_params.get("sortBy")
        favorite = (
            self.request.query_params.get("favorites")
            if self.request.user.is_authenticated
            else None
        )

        if city is not None:
            venues = venues.filter(city=city).filter(menu__isnull=False)

        if favorite is not None:
            venues = venues.filter(favorite_venues__user=self.request.user)

        if kitchen_type is not None and kitchen_type.isnumeric():
            venues = venues.filter(kitchenType=int(kitchen_type))

        if free_delivery is not None and free_delivery == "true":
            venues = venues.filter(Q(deliveryCost=0) | Q(deliveryCost__isnull=True))

        if availability is not None and availability == "true":
            venues = venues.filter(
                Q(openingHours__weekDay=datetime.today().weekday()),
                Q(openingHours__openHour__lt=datetime.now()),
                Q(openingHours__closeHour__gt=datetime.now()),
            )

        if rating is not None and rating.isnumeric():
            venues = venues.annotate(avg_rating=Coalesce(Avg("venueRatings"), 1.0)).filter(
                avg_rating__gt=int(rating) - 0.4
            )

        if order_by is not None:
            if order_by in ["name", "deliveryCost", "deliveryMinimalOrderPrice"]:
                venues = venues.order_by(order_by)
            if order_by == "rating":
                venues = venues.annotate(
                    avg_rating=Coalesce(Avg("venueRatings__rating"), 1.0)
                ).order_by("-avg_rating")

        return venues


@permission_classes([AllowAny])
class VenueRegister(APIView):
    def post(self, request):
        serialized_data = VenueRegisterSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return JsonResponse(serialized_data.data, status=201)


@permission_classes([IsAuthenticatedOrReadOnly])
class VenueDetail(APIView):
    def get_object(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            raise VenueDoesntExists

    def get(self, request, pk):
        venue = self.get_object(pk)
        serialized_data = VenueDetailSerializer(venue)
        return JsonResponse(serialized_data.data)


@permission_classes([IsAuthenticated])
class VenueDetailConfig(APIView):
    @staticmethod
    def update(venue: Venue, data: dict) -> Venue:
        venue_serializer = VenueDetailCorrectSerializer(venue, data=data)

        venue_serializer.is_valid(raise_exception=True)
        venue = venue_serializer.save()
        return venue

    @staticmethod
    def get_venue_by_user(user_id) -> Venue:
        try:
            return Venue.objects.get(owner=user_id)
        except Venue.DoesNotExist:
            raise VenueDoesntExists

    def get(self, request):
        user = self.request.user.pk
        venue = self.get_venue_by_user(user)
        serialized_data = VenueDetailSerializer(venue)
        return JsonResponse(serialized_data.data)

    def patch(self, request, **kwargs):
        #little hack
        if 'image' in request.data:
            request.data.pop('image')
        venue = self.get_venue_by_user(self.request.user.pk)
        new_venue = self.update(venue, request.data)
        new_venue_serializer = VenueDetailCorrectSerializer(instance=new_venue)
        return Response(data=new_venue_serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class KitchenTypesList(APIView):
    def get(self, request):
        kitchen_types = KitchenType.objects.all()
        serialized_data = KitchenTypeSerializer(kitchen_types, many=True)
        return JsonResponse(serialized_data.data, safe=False)


@permission_classes([AllowAny])
class Cities(APIView):
    def get(self, request):
        cities = list(Venue.objects.all().distinct("city").values("city"))
        for i, x in enumerate(cities):
            cities[i]["name"] = x.pop("city")

        return JsonResponse(cities, safe=False)


@permission_classes([IsAuthenticated])
class UserFavoriteVenuesList(APIView):
    def get(self, request):
        venues = Venue.objects.filter(favorite_venues__user=request.user)
        serialized_data = VenueListSerializer(venues, many=True)

        return JsonResponse(serialized_data.data, safe=False)


@permission_classes([IsAuthenticated])
class UserFavoriteVenueView(APIView):
    def post(self, request, pk):
        if UserFavoriteVenue.objects.filter(user=request.user.pk, venue=pk).exists():
            raise UserFavoriteVenueAlreadyExists
        UserFavoriteVenue.objects.create(
            user=request.user, venue=Venue.objects.get(id=pk)
        )

        return JsonResponse({}, safe=False)

    def delete(self, request, pk):
        try:
            UserFavoriteVenue.objects.get(user=request.user, venue=pk).delete()
        except UserFavoriteVenue.DoesNotExist:
            raise UserFavoriteVenueDoesntExist

        return JsonResponse({}, safe=False)


@permission_classes([IsAuthenticated])
class UploadVenueImage(APIView):
    def patch(self, request):
        venue = VenueDetailConfig.get_venue_by_user(request.user.pk)
        serialized_data = VenueImageSerializer(instance=venue, data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return JsonResponse(serialized_data.data, safe=False)
