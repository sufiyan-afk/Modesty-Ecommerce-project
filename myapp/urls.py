from django.urls import path,include
from myapp.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


router.register(
    "categories",
    CategoryViewSet,
    basename="category"
)

router.register(
    "users",
    UserViewSet,
    basename="user"
)

router.register(
    "products",
    ProductViewSet,
    basename="product"
)

router.register(
    "addresses",
    AddressViewSet,
    basename="address"
)


urlpatterns = [
    path("",include(router.urls)),
    path('register/',RegisterAPIView.as_view()),
    path("cart/",CartAPIView.as_view()),
    path("cart/items/",CartItemAPIView.as_view()),
    path("orders/",OrderAPIView.as_view()),
    path("orders/<int:order_id>/",OrderAPIView.as_view()),
    path("payments/",PaymentAPIView.as_view()),
    path("payments/<int:payment_id>/",PaymentAPIView.as_view())
]
