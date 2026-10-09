from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Address,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
)


# ============================================================
# USER SERIALIZER
# ============================================================

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name"
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):

        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )


# ============================================================
# ADDRESS SERIALIZER
# ============================================================

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


# ============================================================
# CATEGORY SERIALIZER
# ============================================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


# ============================================================
# PRODUCT SERIALIZER
# ============================================================

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


# ============================================================
# CART ITEM SERIALIZER
# ============================================================

class CartItemSerializer(serializers.ModelSerializer):

    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = "__all__"


# ============================================================
# CART SERIALIZER
# ============================================================

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "total_amount",
            "created_at",
            "updated_at",
        ]


# ============================================================
# ORDER ITEM SERIALIZER
# ============================================================

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


# ============================================================
# ORDER SERIALIZER
# ============================================================

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "user",
            "address",
            "total_amount",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]


# ============================================================
# PAYMENT SERIALIZER
# ============================================================

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"