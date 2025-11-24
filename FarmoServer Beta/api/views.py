from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
import uuid
from datetime import datetime

def generate_id(prefix):
    return f"{prefix}_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"

@api_view(['POST'])
def register_farmer(request):
    data = request.data.copy()
    data['f_id'] = generate_id('F')
    serializer = FarmerSerializer(data=data)
    if serializer.is_valid():
        farmer = serializer.save()
        Wallet.objects.create(wallet_id=generate_id('W'), f_id=farmer)
        Verification.objects.create(v_id=generate_id('V'), f_id=farmer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_consumer(request):
    data = request.data.copy()
    data['c_id'] = generate_id('C')
    serializer = ConsumerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_farmer(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    try:
        farmer = Farmer.objects.get(phone=phone)
        if check_password(password, farmer.password):
            refresh = RefreshToken()
            refresh['user_id'] = farmer.f_id
            refresh['role'] = 'farmer'
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': FarmerSerializer(farmer).data
            })
    except Farmer.DoesNotExist:
        pass
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login_consumer(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    try:
        consumer = Consumer.objects.get(phone=phone)
        if check_password(password, consumer.password):
            refresh = RefreshToken()
            refresh['user_id'] = consumer.c_id
            refresh['role'] = 'consumer'
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': ConsumerSerializer(consumer).data
            })
    except Consumer.DoesNotExist:
        pass
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def login_admin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        admin = Admin.objects.get(username=username)
        if check_password(password, admin.password):
            refresh = RefreshToken()
            refresh['user_id'] = admin.username
            refresh['role'] = 'admin'
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': AdminSerializer(admin).data
            })
    except Admin.DoesNotExist:
        pass
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        data = request.data.copy()
        data['p_id'] = generate_id('P')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = self.get_queryset()
        category = request.query_params.get('category')
        organic = request.query_params.get('organic')
        search = request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if organic:
            queryset = queryset.filter(organic=organic)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OrderRequestViewSet(viewsets.ModelViewSet):
    queryset = OrderRequest.objects.all()
    serializer_class = OrderRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['order_id'] = generate_id('O')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerRatingViewSet(viewsets.ModelViewSet):
    queryset = FarmerRating.objects.all()
    serializer_class = FarmerRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['r_id'] = generate_id('R')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['prating_id'] = generate_id('PR')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        verification = self.get_object()
        verification.status = 'Approved'
        verification.approved_date = datetime.now()
        verification.approved_by_id = request.data.get('approved_by')
        verification.save()
        return Response(VerificationSerializer(verification).data)
