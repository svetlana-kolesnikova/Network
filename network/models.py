from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Contact(models.Model):
    """Контактная информация узла сети."""

    email: models.EmailField = models.EmailField()
    country: models.CharField = models.CharField(max_length=128)
    city: models.CharField = models.CharField(max_length=128)
    street: models.CharField = models.CharField(max_length=128)
    house_number: models.CharField = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.country}, {self.city}"


class Product(models.Model):
    """Продукт электроники."""

    name: models.CharField = models.CharField(max_length=255)
    model: models.CharField = models.CharField(max_length=255)
    release_date: models.DateField = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """Звено сети продаж электроники."""

    name: models.CharField = models.CharField(max_length=255)
    contact: models.OneToOneField = models.OneToOneField(Contact, on_delete=models.CASCADE)
    products: models.ManyToManyField = models.ManyToManyField(Product, related_name="nodes")

    supplier: models.ForeignKey = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients",
    )

    debt: models.DecimalField = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        """Валидация отсутствия циклов в иерархии."""
        node = self.supplier
        while node:
            if node == self:
                raise ValidationError("Циклическая зависимость поставщиков запрещена.")
            node = node.supplier

    @property
    def level(self) -> int:
        """Вычисление уровня иерархии."""
        level = 0
        node = self.supplier
        while node:
            level += 1
            node = node.supplier
        return level

    def __str__(self) -> str:
        return self.name
