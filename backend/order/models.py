from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from authenticator.models import User
from menu.models import MenuItem, MenuAddon
from venue.models import Venue


class OrderStatus:
    NEW = "new"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"

    CHOICES = (
        (NEW, "new"),
        (ACCEPTED, "accepted"),
        (REJECTED, "rejected"),
        (COMPLETED, "completed"),
    )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=100, choices=OrderStatus.CHOICES, default=OrderStatus.NEW
    )

    def __str__(self):
        return f"User: {self.user.username}, Venue: {self.venue.name}"


class DeliveryInformation(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    houseNumber = models.CharField(max_length=100)
    apartmentNumber = models.CharField(max_length=100, null=True, blank=True)
    contact_phone = models.CharField(max_length=100)
    information = models.CharField(max_length=100, null=True, blank=True)
    order = models.OneToOneField(
        Order, related_name="delivery", null=True, blank=True, on_delete=models.CASCADE
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderItems"
    )
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    addons = models.ManyToManyField(MenuAddon, blank=True)
