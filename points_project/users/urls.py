from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/modify-points/', views.modify_points, name='modify_points'),
    path('', views.homepage, name='homepage'),
    path('points/', views.user_points, name='user_points'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('register/', views.register, name='register'),
]
