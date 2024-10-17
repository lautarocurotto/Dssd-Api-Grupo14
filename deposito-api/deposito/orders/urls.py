from django.urls import path
from .views import OrderListView, ReserveOrderView, RegisterMaterialProviderView, DeliverOrderAPIView, CreateOrderAPIView, MaterialListAPIView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/reserve/<int:pk>/', ReserveOrderView.as_view(), name='reserve-order'),
    path('deliver-order/<int:pk>/', DeliverOrderAPIView.as_view(), name='deliver_order'),
    path('create-order/', CreateOrderAPIView.as_view(), name='create_order'),
    path('register-material/', RegisterMaterialProviderView.as_view(), name='register-material-provider'),
    path('materials/', MaterialListAPIView.as_view(), name='material-list'),
]
