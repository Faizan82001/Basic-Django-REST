from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from .views import RegistrationView, CustomerDetail, CustomerOrderList

urlpatterns = [
    path('auth/login', TokenObtainPairView.as_view(), name='login'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/verify', TokenVerifyView.as_view(), name='token-verify'),
    path('auth/register', RegistrationView.as_view(), name='registration'),
    path('profile/<uuid:pk>', CustomerDetail.as_view(), name='profile'),
    path("profile/<uuid:pk>/orders", CustomerOrderList.as_view(), name='customer-order-list'),
]