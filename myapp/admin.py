from django.contrib import admin
from .models import (
    User,
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
# ADDRESS ADMIN
# ============================================================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "city",
        "state",
        "pincode",
        "is_default",
        "created_at",
    )

    list_filter = (
        "city",
        "state",
        "is_default",
    )

    search_fields = (
        "user__username",
        "user__email",
        "full_name",
        "phone",
        "city",
        "pincode",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# CATEGORY ADMIN
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# PRODUCT ADMIN
# ============================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "quantity",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "category__name",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# CART ADMIN
# ============================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "created_at",
        "updated_at",
    )



    ordering = (
        "-created_at",
    )


# ============================================================
# CART ITEM ADMIN
# ============================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
    )


# ============================================================
# ORDER ADMIN
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order_number",
        "user",
        "address",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "order_number",
        "user__username",
        "user__email",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# ORDER ITEM ADMIN
# ============================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "product_name",
        "price",
        "quantity",
        "subtotal",
        "created_at",
    )

    search_fields = (
        "product_name",
        "order__order_number",
    )


# ============================================================
# PAYMENT ADMIN
# ============================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "amount",
        "payment_method",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "payment_method",
        "status",
    )

    search_fields = (
        "order__order_number",
        "transaction_id",
    )

    ordering = (
        "-created_at",
    )
