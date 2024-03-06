from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from .models import Cart, CartItem
from .errors import (
    CartDoesntExist,
    CartItemDoesntExist,
    CartAlreadyExists,
    CartItemAlreadyExists,
)


@permission_classes([IsAuthenticated])
class CartView(APIView):
    @staticmethod
    def get_cart(self, user, pk):
        try:
            return Cart.objects.get(user=user, venue=pk)
        except Cart.DoesNotExist:
            raise CartDoesntExist

    def post(self, request, pk):
        if Cart.objects.filter(user=request.user, venue=pk):
            raise CartAlreadyExists
        serialized_data = CartCreateSerializer(
            data=request.data, context={"request": request, "pk": pk}
        )
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return JsonResponse(serialized_data.data)

    def get(self, request, pk):
        cart = self.get_cart(self, request.user, pk)
        serialized_data = CartSerializer(cart)
        return JsonResponse(serialized_data.data)

    def delete(self, request, pk):
        self.get_cart(self, request.user, pk).delete()
        return JsonResponse({}, status=204, safe=False)


@permission_classes([IsAuthenticated])
class CartItemView(APIView):
    @staticmethod
    def get_cart_item(self, cart, item):
        try:
            return cart.cartItems.get(id=item)
        except CartItem.DoesNotExist:
            raise CartItemDoesntExist

    def patch(self, request, pk, item):
        cart = CartView.get_cart(self, request.user, pk)
        cart_item = self.get_cart_item(self, cart, item)
        serialized_data = CartItemUpdateSerializer(
            cart_item,
            data=request.data,
            partial=True,
            context={"request": request, "pk": pk},
        )
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        response = CartSerializer(cart)
        return JsonResponse(response.data, status=200)

    def delete(self, request, pk, item):
        cart = CartView.get_cart(self, request.user, pk)
        self.get_cart_item(self, cart, item).delete()
        if cart.cartItems.count() == 0:
            cart.delete()
            return JsonResponse({}, status=200)
        response = CartSerializer(cart)
        return JsonResponse(response.data, status=200)


@permission_classes([IsAuthenticated])
class CartItemCreateView(APIView):
    def post(self, request, pk):
        cart = CartView.get_cart(self, request.user, pk)
        serialized_data = CartItemCreateSerializer(
            data=request.data, context={"request": request, "pk": pk}
        )
        serialized_data.is_valid(raise_exception=True)
        for cart_item in cart.cartItems.all():
            if (
                serialized_data.validated_data["addons"] == list(cart_item.addons.all())
                and serialized_data.validated_data["item"] == cart_item
            ):
                raise CartItemAlreadyExists
        serialized_data.save(cart=cart)
        response = CartSerializer(cart)
        return JsonResponse(response.data, status=201)
