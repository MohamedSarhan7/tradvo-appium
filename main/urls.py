from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('dashboard/', views.AllAppsView.as_view(), name='dashboard'),
    path('app/create/', views.AppCreateView.as_view(), name='create'),
    path('app-update/<int:pk>', views.AppUpdateView.as_view(), name='app-update'),
    path('app-delete/<int:pk>',views.AppDeleteView.as_view(),name="app-delete"),
    path('test/<int:pk>', views.start_appium_test_view, name='run_appium_test'),
]
