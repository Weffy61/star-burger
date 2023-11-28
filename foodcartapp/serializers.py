from rest_framework.serializers import ModelSerializer, ListField
from rest_framework import serializers

from .models import OrderItem, Order


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = ListField(
        child=OrderItemSerializer(),
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'products', 'firstname', 'lastname', 'phonenumber', 'address']
