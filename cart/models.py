from django.db import models
from menu.models import MenuItem, MenuAddon
from authenticator.models import User
from venue.models import Venue
from django.core.validators import MinValueValidator
from django.utils import timezone


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT)
    creationDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User: {self.user.username}, Venue: {self.venue.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartItems")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    addons = models.ManyToManyField(MenuAddon, blank=True)

    def __str__(self):
        return f"Item: {self.item}, Cart: {self.cart}"
