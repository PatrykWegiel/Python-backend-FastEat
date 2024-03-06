from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .errors import UserUnauthorized
from .models import OrderStatus
from .serializers import *


@permission_classes([AllowAny])
class OrderClientView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return JsonResponse({}, status=200, safe=False)
        orders = Order.objects.filter(user=request.user)
        order_serializer = OrderSerializer(instance=orders, many=True)
        return JsonResponse(order_serializer.data, status=200, safe=False)

    def post(self, request):
        if request.user.is_anonymous:
            raise UserUnauthorized

        order_serializer = OrderCreateSerializer(
            data=request.data, context={"request": request}
        )
        order_serializer.is_valid(raise_exception=True)
        new_order = order_serializer.save()

        order_serializer = OrderSerializer(instance=new_order)
        return JsonResponse(order_serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
class OrderVenueView(APIView):
    @staticmethod
    def get_venue(user_id) -> Venue:
        try:
            return Venue.objects.get(owner=user_id)
        except Venue.DoesNotExist:
            raise UserUnauthorized

    @staticmethod
    def get_order(order_pk, venue) -> Order:
        try:
            return Order.objects.get(pk=order_pk, venue=venue)
        except Order.DoesNotExist:
            raise UserUnauthorized

    def get(self, request):
        venue = self.get_venue(self.request.user.pk)
        orders = Order.objects.filter(venue=venue).order_by('-creationDate')
        order_serializer = OrderSerializer(instance=orders, many=True)
        return JsonResponse(order_serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
class OrderVenueAcceptView(OrderVenueView):
    def post(self, request, order_pk):
        venue = self.get_venue(self.request.user.pk)
        order = self.get_order(order_pk, venue)
        order.status = OrderStatus.ACCEPTED
        order.save(update_fields=["status"])

        send_mail(
            'Zamówienie zostało przyjęte',
            'Twoje zamówienie zostało przyjęte',
            'fasteatcompany@example.com',
            [order.user.email],
            fail_silently=False,
        )

        order_serializer = OrderSerializer(instance=order)
        return JsonResponse(order_serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
class OrderVenueCompleteView(OrderVenueView):
    def post(self, request, order_pk):
        venue = self.get_venue(self.request.user.pk)
        order = self.get_order(order_pk, venue)
        order.status = OrderStatus.COMPLETED
        order.save(update_fields=["status"])

        order_serializer = OrderSerializer(instance=order)
        return JsonResponse(order_serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
class OrderVenueRejectView(OrderVenueView):
    def post(self, request, order_pk):
        venue = self.get_venue(self.request.user.pk)
        order = self.get_order(order_pk, venue)
        order.status = OrderStatus.REJECTED
        order.save(update_fields=["status"])

        send_mail(
            'Zamówienie zostało odrzucone',
            'Twoje zamówienie zostało odrzucone',
            'fasteatcompany@example.com',
            [order.user.email],
            fail_silently=False,
        )

        order_serializer = OrderSerializer(instance=order)
        return JsonResponse(order_serializer.data, status=200, safe=False)
