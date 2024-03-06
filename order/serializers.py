from rest_framework import serializers

from authenticator.models import User
from menu.models import MenuItem, MenuAddon
from menu.serializers import MenuItemSerializer
from venue.models import Venue
from venue.serializers import VenueDetailSerializer
from .models import Order, OrderItem, DeliveryInformation


class OrderMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price"]


class OrderMenuAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuAddon
        fields = ["id", "name", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    addons = OrderMenuAddonSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ["item", "addons", "amount"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        item_id = data.pop("item")
        item = MenuItem.objects.get(pk=item_id)
        item_data = MenuItemSerializer(item).data
        data["item"] = item_data
        return data


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["item", "addons", "amount"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        item_id = data.pop("item")
        item = MenuItem.objects.get(pk=item_id)
        item_data = MenuItemSerializer(item).data
        data["item"] = item_data
        return data


class DeliveryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInformation
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    orderItems = OrderItemCreateSerializer(many=True)
    delivery = DeliveryInformationSerializer()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "user", "creationDate", "status"]

    def create(self, validated_data):
        user = self.context["request"].user
        order = Order.objects.create(
            user=user,
            venue=validated_data.pop("venue"),
        )
        DeliveryInformation.objects.create(
            order=order, **validated_data.pop("delivery")
        )

        order_item = validated_data.pop("orderItems")
        for i in order_item:
            item_addons = i.pop("addons")
            OrderItem.objects.create(order=order, **i).addons.set(item_addons)

        return order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        venue_id = data.pop("venue")
        venue = Venue.objects.get(pk=venue_id)
        venue_data = VenueDetailSerializer(venue).data
        data["venue"] = venue_data
        return data


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True)
    delivery = DeliveryInformationSerializer()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "user", "creationDate", "status"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        venue_id = data.pop("venue")
        user_id = data.pop("user")
        venue = Venue.objects.get(pk=venue_id)
        user = User.objects.get(pk=user_id)
        venue_data = VenueDetailSerializer(venue).data
        data["venue"] = venue_data
        data["user"] = {}
        data["user"]['name'] = user.username
        data["user"]['email'] = user.email
        return data
