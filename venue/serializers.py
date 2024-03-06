from django.contrib.auth.models import Group
from django.db.models import Avg
from django.db.models.functions import Coalesce, Round
from rest_framework import serializers

from authenticator.models import User
from authenticator.serializers import UserRegisterSerializer
from .models import Venue, KitchenType, UserFavoriteVenue


class KitchenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenType
        fields = ["id", "kitchenType"]


class VenueListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(
        max_length=None, allow_null=True, required=False
    )
    kitchenType = KitchenTypeSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, venue):
        return venue.venueRatings.all().aggregate(
            rating__avg=Coalesce(Round(Avg("rating")), 1.0)
        )["rating__avg"]

    class Meta:
        model = Venue
        fields = [
            "id",
            "name",
            "kitchenType",
            "description",
            "image",
            "deliveryCost",
            "deliveryMinimalOrderPrice",
            "menu",
            "avg_rating",
        ]


class AuthVenueListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(
        max_length=None, allow_null=True, required=False
    )
    kitchenType = KitchenTypeSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField("is_favorite")

    def get_avg_rating(self, venue):
        return venue.venueRatings.all().aggregate(
            rating__avg=Coalesce(Round(Avg("rating")), 1.0)
        )["rating__avg"]

    def is_favorite(self, venue):
        return venue.favorite_venues.filter(user=self.context["request"].user).exists()

    class Meta:
        model = Venue
        fields = [
            "id",
            "name",
            "kitchenType",
            "description",
            "image",
            "deliveryCost",
            "deliveryMinimalOrderPrice",
            "menu",
            "avg_rating",
            "favorite",
        ]


class VenueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class VenueDetailCorrectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Venue
        fields = [
            "name",
            "description",
            "kitchenType",
            "deliveryCost",
            "deliveryMinimalOrderPrice",
            "zipCode",
            "street",
            "city",
            "phoneNumber",
            "image",
        ]


class VenueRegisterSerializer(serializers.ModelSerializer):
    owner = UserRegisterSerializer()

    class Meta:
        model = Venue
        fields = [
            "name",
            "zipCode",
            "street",
            "city",
            "phoneNumber",
            "kitchenType",
            "owner",
        ]

    def create(self, validated_data):
        owner_data = validated_data.pop("owner")
        user = User.objects.create_user(**owner_data)
        kitchen_type = validated_data.pop("kitchenType")
        venue = Venue.objects.create(owner=user, **validated_data)
        venue.kitchenType.set(kitchen_type)
        user.groups.add(Group.objects.get(name="venue_manager"))
        return venue

    def to_representation(self, instance):
        self.fields["kitchenType"] = KitchenTypeSerializer(many=True)
        return super().to_representation(instance)


class UserFavoriteVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteVenue
        fields = ["venue"]


class VenueImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = Venue
        fields = ["image"]
