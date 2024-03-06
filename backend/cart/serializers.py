from rest_framework import serializers
from .models import Cart, CartItem
from menu.models import MenuItem, MenuAddon, MenuCategory
from .errors import WrongMenuItem, WrongItemAddon
from venue.models import Venue


class CartMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price"]


class CartMenuAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuAddon
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    item = CartMenuItemSerializer()
    addons = CartMenuAddonSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ["id", "item", "addons", "amount"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sum"] = (
            sum(addon["price"] for addon in data["addons"]) + data["item"]["price"]
        ) * data["amount"]
        return data


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["cartItems"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sum"] = sum(item["sum"] for item in data["cartItems"])
        return data


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["item", "addons", "amount"]

    def validate(self, data):
        super().validate(data)
        venue = Venue.objects.get(pk=self.context["pk"])
        try:
            venue.menu.categories.get(items__id=data["item"].id)
        except MenuCategory.DoesNotExist:
            raise WrongMenuItem
        if "addons" in data:
            try:
                for addon in data["addons"]:
                    MenuItem.objects.get(id=data["item"].id).addons.get(id=addon.id)
            except MenuAddon.DoesNotExist:
                raise WrongItemAddon(
                    detail=f"Addon(id={addon.id}) cannot be selected for this item"
                )
        return data

    def to_representation(self, instance):
        serializer = CartItemSerializer(instance)
        return serializer.data


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["addons", "amount"]

    def validate_addons(self, data):
        try:
            for addon in data:
                MenuItem.objects.get(id=self.instance.item.id).addons.get(id=addon.id)
        except MenuAddon.DoesNotExist:
            raise WrongItemAddon(
                detail=f"Addon(id={addon.id}) cannot be selected for this item"
            )
        return data

    def to_representation(self, instance):
        serializer = CartItemSerializer(instance)
        return serializer.data


class CartCreateSerializer(serializers.ModelSerializer):
    items = CartItemCreateSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["items"]

    def validate_items(self, data):
        venue = Venue.objects.get(pk=self.context["pk"])
        for item in data:
            try:
                venue.menu.categories.get(items__id=item["item"].id)
            except MenuCategory.DoesNotExist:
                raise WrongMenuItem
            if "addons" in item:
                try:
                    for addon in item["addons"]:
                        MenuItem.objects.get(id=item["item"].id).addons.get(id=addon.id)
                except MenuAddon.DoesNotExist:
                    raise WrongItemAddon(
                        detail=f"Addon(id={addon.id}) cannot be selected for this item"
                    )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        venue = Venue.objects.get(pk=self.context["pk"])
        cart_items = validated_data.pop("items")
        cart = Cart.objects.create(user=user, venue=venue)
        for item in cart_items:
            if "addons" in item:
                item_addons = item.pop("addons")
                CartItem.objects.create(cart=cart, **item).addons.set(item_addons)
            else:
                CartItem.objects.create(cart=cart, **item)
        return cart

    def to_representation(self, instance):
        serializer = CartSerializer(instance)
        return serializer.data
