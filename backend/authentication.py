from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Users
from .serializers import UsersSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UsersSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response({'error': 'Identifier and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from django.db.models import Q
        user = Users.objects.get(Q(user_id=identifier) | Q(phone=identifier) | Q(email=identifier))
        
        if hasattr(user, 'credentials') and user.credentials.password:
            if user.credentials.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UsersSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Users.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def verify_wallet_pin(request):
    wallet_id = request.data.get('wallet_id')
    pin = request.data.get('pin')
    
    if not wallet_id or not pin:
        return Response({'error': 'Wallet ID and PIN required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from .models import Wallet
        wallet = Wallet.objects.get(wallet_id=wallet_id, user=request.user)
        if wallet.check_pin(pin):
            return Response({'verified': True}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
    except Wallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
