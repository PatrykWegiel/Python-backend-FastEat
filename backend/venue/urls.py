from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("venues/", views.VenueList.as_view()),
    re_path("^venues/(?P<city>.+)/$", views.VenueList.as_view()),
    path("venues/register", views.VenueRegister.as_view()),
    path("venues/<int:pk>", views.VenueDetail.as_view()),
    path("venues/config", views.VenueDetailConfig.as_view()),
    path("venues/kitchen/list", views.KitchenTypesList.as_view()),
    path("venues/<int:pk>/", include("cart.urls")),
    path("cities/", views.Cities.as_view()),
    path("venues/favorites", views.UserFavoriteVenuesList.as_view()),
    path("venues/favorites/<int:pk>", views.UserFavoriteVenueView.as_view()),
    path("venues/config/image", views.UploadVenueImage.as_view()),
]
