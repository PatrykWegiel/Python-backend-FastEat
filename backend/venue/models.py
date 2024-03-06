import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models
from django_resized import ResizedImageField

from authenticator.models import User
from menu.models import Menu


def venue_image_upload(instance, filename):
    path = "venue/logo/"
    file_extension = filename.split(".")[1]
    format = str(instance.id) + "_" + instance.name + "." + file_extension
    return os.path.join(path, format)


class KitchenType(models.Model):
    kitchenType = models.CharField(max_length=100)

    def __str__(self):
        return self.kitchenType


class Venue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=512, blank=True)
    image = ResizedImageField(
        size=[500, 300],
        upload_to=venue_image_upload,
        null=True,
        blank=True,
        force_format="PNG",
    )
    kitchenType = models.ManyToManyField(KitchenType)
    deliveryArea = models.PolygonField(null=True, blank=True)
    deliveryCost = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0
    )
    deliveryMinimalOrderPrice = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0
    )
    zipCode = models.CharField(max_length=6)
    street = models.CharField(max_length=60)
    city = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)
    menu = models.ForeignKey(
        Menu, on_delete=models.SET_NULL, related_name="venues", null=True
    )

    def __str__(self):
        return self.name


class VenueBusinessTime(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.RESTRICT, null=True, related_name="openingHours"
    )
    weekDay = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    openHour = models.TimeField(null=True)
    closeHour = models.TimeField(null=True)


class VenueRating(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.RESTRICT, null=False, related_name="venueRatings"
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.CharField(max_length=512, blank=True)


class UserFavoriteVenue(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.RESTRICT, null=False, related_name="favorite_venues"
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=False, related_name="favorite_by"
    )

    def __str__(self):
        return f"User: {self.user}, Venue: {self.venue}"
