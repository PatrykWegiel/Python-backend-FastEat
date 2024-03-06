from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.CartView.as_view()),
    path("cart/edit/<item>", views.CartItemView.as_view()),
    path("cart/edit", views.CartItemCreateView.as_view()),
]
