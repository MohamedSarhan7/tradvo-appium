from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('dashboard/', views.test, name='dashboard'),

]