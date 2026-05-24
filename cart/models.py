from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Flavor(models.Model):
    name = models.CharField(
        max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    quantity = models.PositiveIntegerField()

    max_flavor_select = models.PositiveIntegerField(
        default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    flavors = models.ManyToManyField(Flavor)

    def __str__(self):
        return self.name


class Cart(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
        )

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1)

    flavors = models.ManyToManyField(Flavor)

    def __str__(self):
        return self.item.name
