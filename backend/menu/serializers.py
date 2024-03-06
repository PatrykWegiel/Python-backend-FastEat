from rest_framework import serializers
from menu.models import Menu, MenuCategory, MenuItem, MenuAddon


class MenuAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuAddon
        fields = ["id", "name", "description", "sequence", "price", "image"]
        read_only_fields = ["id", "image"]


class MenuItemSerializer(serializers.ModelSerializer):
    addons = MenuAddonSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "sequence", "price", "addons", "image"]
        read_only_fields = ["id", "image"]

    def _create_addons(self, item, addons_data):
        for addon_data in addons_data:
            MenuAddon(item=item, **addon_data).save()

    def create(self, validated_data):
        addons_data = validated_data.pop("addons")
        item = MenuItem.objects.create(**validated_data)
        self._create_addons(item, addons_data)
        return item

    def _update_extra(self, instance, data):
        instance.name = data.get("name", instance.name)
        instance.description = data.get("description", instance.description)
        instance.sequence = data.get("sequence", instance.sequence)
        instance.price = data.get("price", instance.price)
        # instance.image = data.get('sequence', instance.image)

        return instance

    def _update_addons(self, addons, addons_data):
        for instance, data in zip(addons, addons_data):
            instance = self._update_extra(instance, data)
            instance.save()

    def update(self, instance, validated_data):
        instance = self._update_extra(instance, validated_data)
        instance.save()
        self._update_addons(
            instance.addons.all(), validated_data.get("addons", instance.addons.all())
        )

        return instance


class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = MenuCategory
        fields = ["id", "name", "description", "sequence", "items"]
        read_only_fields = ["id"]

    def _create_addons(self, item, addons_data):
        for addon_data in addons_data:
            MenuAddon(item=item, **addon_data).save()

    def _create_items(self, category, items_data):
        for item_data in items_data:
            addons_data = item_data.pop("addons")
            item = MenuItem.objects.create(category=category, **item_data)
            self._create_addons(item, addons_data)

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        category = MenuCategory.objects.create(**validated_data)
        self._create_items(category, items_data)

        return category

    def _update_extra(self, instance, data):
        instance.name = data.get("name", instance.name)
        instance.description = data.get("description", instance.description)
        instance.sequence = data.get("sequence", instance.sequence)
        instance.price = data.get("price", instance.price)
        # instance.image = data.get('sequence', instance.image)

        return instance

    def _update_addons(self, addons, addons_data):
        for instance, data in zip(addons, addons_data):
            instance = self._update_extra(instance, data)
            instance.save()

    def _update_items(self, items, items_data):
        for instance, data in zip(items, items_data):
            instance = self._update_extra(instance, data)
            instance.save()
            self._update_addons(
                instance.addons.all(), data.get("addons", instance.addons.all())
            )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.sequence = validated_data.get("sequence", instance.sequence)
        instance.save()
        self._update_items(
            instance.items.all(), validated_data.get("items", instance.items.all())
        )
        return instance


class MenuSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "description", "categories"]
        read_only_fields = ["id"]

    def _create_addons(self, item, addons_data):
        for addon_data in addons_data:
            MenuAddon(item=item, **addon_data).save()

    def _create_items(self, category, items_data):
        for item_data in items_data:
            addons_data = item_data.pop("addons")
            item = MenuItem.objects.create(category=category, **item_data)
            self._create_addons(item, addons_data)

    def _create_category(self, menu, categories_data):
        for category_data in categories_data:
            items_data = category_data.pop("items")
            category = MenuCategory.objects.create(menu=menu, **category_data)
            self._create_items(category, items_data)

    def create(self, validated_data):
        categories_data = validated_data.pop("categories")
        menu = Menu.objects.create(**validated_data)
        self._create_category(menu, categories_data)

        return menu

    def _update_extra(self, instance, data):
        instance.name = data.get("name", instance.name)
        instance.description = data.get("description", instance.description)
        instance.sequence = data.get("sequence", instance.sequence)
        instance.price = data.get("price", instance.price)
        # instance.image = data.get('sequence', instance.image)

        return instance

    def _update_addons(self, addons, addons_data):
        for instance, data in zip(addons, addons_data):
            instance = self._update_extra(instance, data)
            instance.save()

    def _update_items(self, items, items_data):
        for instance, data in zip(items, items_data):
            instance = self._update_extra(instance, data)
            instance.save()
            self._update_addons(
                instance.addons.all(), data.get("addons", instance.addons.all())
            )

    def _update_category(self, categories, categories_data):
        for instance, data in zip(categories, categories_data):
            instance.name = data.get("name", instance.name)
            instance.description = data.get("description", instance.description)
            instance.sequence = data.get("sequence", instance.sequence)
            instance.save()
            self._update_items(
                instance.items.all(), data.get("items", instance.items.all())
            )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        self._update_category(
            instance.categories.all(),
            validated_data.get("categories", instance.categories.all()),
        )

        instance.save()
        return instance


class MenuItemImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = MenuItem
        fields = ["image"]


class MenuAddonImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = MenuAddon
        fields = ["image"]
