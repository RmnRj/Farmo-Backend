from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderRequestViewSet)
router.register(r'farmer-ratings', views.FarmerRatingViewSet)
router.register(r'product-ratings', views.ProductRatingViewSet)
router.register(r'verifications', views.VerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/farmer/', views.register_farmer),
    path('auth/register/consumer/', views.register_consumer),
    path('auth/login/farmer/', views.login_farmer),
    path('auth/login/consumer/', views.login_consumer),
    path('auth/login/admin/', views.login_admin),
]
