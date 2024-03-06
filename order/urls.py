from django.urls import path

from order.views import (
    OrderClientView,
    OrderVenueAcceptView,
    OrderVenueRejectView,
    OrderVenueCompleteView,
    OrderVenueView,
)

urlpatterns = [
    path("orders", OrderClientView.as_view()),
    path("myorders", OrderVenueView.as_view()),
    path("myorders/<int:order_pk>/accept", OrderVenueAcceptView.as_view()),
    path("myorders/<int:order_pk>/rejact", OrderVenueRejectView.as_view()),
    path("myorders/<int:order_pk>/complete", OrderVenueCompleteView.as_view()),
]
