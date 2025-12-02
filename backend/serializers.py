from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    Users, Credentials, Wallet, Transaction, Product, ProductMedia,
    ProductRating, FarmerRating, Verification, OrderRequest, OrdProdLink
)


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Users.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CredentialsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Credentials
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        credential = Credentials.objects.create(**validated_data)
        if password:
            credential.set_password(password)
            credential.save()
        return credential


class WalletSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, required=False, min_length=4, max_length=6)

    class Meta:
        model = Wallet
        fields = '__all__'
        extra_kwargs = {'pin': {'write_only': True}}

    def create(self, validated_data):
        pin = validated_data.pop('pin', None)
        wallet = Wallet.objects.create(**validated_data)
        if pin:
            wallet.set_pin(pin)
            wallet.save()
        return wallet

    def update(self, instance, validated_data):
        pin = validated_data.pop('pin', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if pin:
            instance.set_pin(pin)
        instance.save()
        return instance


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
