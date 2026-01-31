# network/serializers.py

from rest_framework import serializers
from .models import NetworkNode, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор контактов."""

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов."""

    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор звена сети с вложенными сущностями."""

    contact = ContactSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt", "created_at")


    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        products_data = validated_data.pop("products")

        contact = Contact.objects.create(**contact_data)
        node = NetworkNode.objects.create(contact=contact, **validated_data)

        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            node.products.add(product)

        return node