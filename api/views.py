from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from api.models import *
from . serializers import UserSerializer, LandSerializer, TransactionSerializer

# User Registration API
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    data['password'] = make_password(data['password'])  # Hash password
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Land CRUD API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_land(request):
    if request.method == 'GET':
        lands = Land.objects.all()
        serializer = LandSerializer(lands, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def land_detail(request, id):
    try:
        land = Land.objects.get(pk=id)
    except Land.DoesNotExist:
        return Response({'error': 'Land not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LandSerializer(land)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LandSerializer(land, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        land.delete()
        return Response({'message': 'Land deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Transaction API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_transaction(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
