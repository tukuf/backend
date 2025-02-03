from Land.views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Land import views
# from . import views

urlpatterns = [
    #register 
    path('api/user/', views.register_user, name='register_user'),

path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),
        path('add_land/', views.add_land, name='add_land'),
# new
    path('login/', views.login_view, name='login'),
    path('user_info/', views.user_info, name='user_info'),
    # user endpoint
    path('user/',views.manage_user),
    path('user/<int:id>/', views.manage_user),

    # land endpoint
    path('land/', views.manage_land),
    path('land/<int:id>/', views.manage_land),

    path('inquiry/', views.manage_inquiry),
    path('inquiry/<int:id>/', views.manage_inquiry),

    path('transaction/', views.manage_transaction),
    path('transaction/<int:id>/', views.manage_transaction),

    path('reviews/', views.manage_review),
    path('reviews/<int:id>/',  views.manage_review),
    
     path('notification/', views.manage_notification),
    path('notification/<int:id>/', views.manage_notification),



]