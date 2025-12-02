from rest_framework import serializers
from .models import (
    Users, Credentials, Wallet, Transaction, Product, ProductMedia,
    ProductRating, FarmerRating, Verification, OrderRequest, OrdProdLink
)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = '__all__'
        extra_kwargs = {'password_hash': {'write_only': True}}


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    media = ProductMediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class FarmerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerRating
        fields = '__all__'


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = '__all__'


class OrdProdLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdProdLink
        fields = '__all__'


class OrderRequestSerializer(serializers.ModelSerializer):
    order_items = OrdProdLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrderRequest
        fields = '__all__'
