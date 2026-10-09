import razorpay
from django.conf import settings
from django.db import transaction
import uuid
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.serializers import *
from rest_framework.permissions import AllowAny, IsAdminUser , IsAuthenticated



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get_permissions(self):

        if self.action in ["list","retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):

        if self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes  = [IsAdminUser]

        return [permission() for permission in permission_classes]



class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)



class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)



class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def patch(self , request):
        cart_item_id = request.data.get("cart_item")
        quantity = request.data.get("quantity")

        cart_item = CartItem.objects.get(
            id = cart_item_id,
            cart__user = request.user
        )

        if quantity <= 0:
            return Response(
                {"error": "quantity must be greater than 0"},
                status = status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data , status = status.HTTP_200_OK)

    def delete(self , request):
        cart_item_id = request.data.get("cart_item")

        cart_item = CartItem.objects.get(
            id = cart_item_id,
            cart__user = request.user
        )
        cart_item.delete()

        return Response(
            {"message":"Cart item removed successfully"},
            status = status.HTTP_204_NO_CONTENT
        )


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request , order_id = None):

        if order_id:
            order = Order.objects.get(
                id = order_id,
                user = request.user
            )

            serializer = OrderSerializer(order)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        orders = Order.objects.filter(user = request.user)

        serializer = OrderSerializer(orders , many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        address_id = request.data.get("address")

        cart = Cart.objects.get(user=request.user)

        if not cart.items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        address = Address.objects.get(
            id=address_id,
            user=request.user
        )
        with transaction.atomic():

            order = Order.objects.create(
                order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
                user=request.user,
                address=address,
                total_amount=cart.total_amount,
                status="PENDING"
            )

            for cart_item in cart.items.all():

                OrderItem.objects.create(
                    order = order,
                    product = cart_item.product,
                    product_name = cart_item.product.name,
                    price = cart_item.product.price,
                    quantity = cart_item.quantity,
                    subtotal = cart_item.subtotal
                )
            cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,payment_id=None):
        if payment_id:
            payment = Payment.objects.get(
                id = payment_id,
                order__user = request.user
            )
            serializer = PaymentSerializer(payment)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        payments = Payment.objects.filter(
            order__user = request.user
        )

        serializer = PaymentSerializer(
            payments,
            many = True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


    def post(self , request):
        order_id = request.data.get("order")
        method = request.data.get("method")

        order = Order.objects.get(
            id = order_id,
            user = request.user
        )

        if Payment.objects.filter(order=order).exists():
            return Response(
                {"error":"Payment already exists for this order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        razorpay_order = client.order.create({
            "amount":int(order.total_amount * 100),
            "currency":"INR",
            "receipt": order.order_number
        })

        payment = Payment.objects.create(
            order = order ,
            razorpay_order_id = razorpay_order["id"],
            amount = order.total_amount,
            payment_method = method,
            status = "PENDING"
        )

        serializer = PaymentSerializer(payment)

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )
