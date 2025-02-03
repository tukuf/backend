from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, redirect
from .forms import LandForm

#added for registering
from .serializers import RegisterUserSerializer

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#added for login
@api_view(['POST'])
def login_view(request):
    # Your JWT login logic here (using simple JWT)
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Redirect based on user type
        if user.user_type == 'landowner':
            return Response({'access_token': str(access_token), 'redirect_url': '/uploadland'})
        elif user.user_type == 'buyer':
            return Response({'access_token': str(access_token), 'redirect_url': '/buyland'})
        elif user.user_type == 'agent':
            return Response({'access_token': str(access_token), 'redirect_url': '/reviewpage'})

    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
def user_info(request):
    user = request.user
    return Response(UserSerializer(user).data)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Mtumiaji atalogin moja kwa moja baada ya kusajili
            return redirect('dashboard')  # Badilisha 'dashboard' na URL ya home yako
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Create your views here.
def generic_api(model_class, class_serializer):
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    def api(request, id=None):
        if request.method == 'GET':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = class_serializer(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'Message': 'Object not found'}, status=404)
            else:
                instances = model_class.objects.all()
                serializer = class_serializer(instances, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = class_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        elif request.method == 'PUT':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = class_serializer(instance, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=400)
                except model_class.DoesNotExist:
                    return Response({'Message': 'Object not found'}, status=404)

        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'Message': 'Object deleted successfully'}, status=204)
                except model_class.DoesNotExist:
                    return Response({'Message': 'Object not found'}, status=404)

        return Response({'Message': 'Invalid request'}, status=400)

    return api  

# NumericPasswordValidator

class LandViewSet(ModelViewSet):
    queryset = Land.objects.all()
    serializer_class = LandSerializer

#add land
from django.shortcuts import render, redirect
from .forms import LandForm

def add_land(request):
    if request.method == 'POST':
        form = LandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_lands')  # Au rudi sehemu unayotaka
    else:
        form = LandForm()
    return render(request, 'land_app/add_land.html', {'form': form})
# # login
# def example_view(request):
#     return render(request, 'Land/example.html')



# Define your views
manage_user = generic_api(User, UserSerializer)
manage_transaction = generic_api(Transaction, TransactionSerializer)
manage_inquiry = generic_api(Inquiry, InquirySerializer)
manage_land = generic_api(Land, LandSerializer)
manage_review = generic_api(Review, ReviewSerializer)
manage_notification = generic_api(Notification, NotificationSerializer)

