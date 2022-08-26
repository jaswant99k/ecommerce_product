from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('users/<int:pk>/', views.UsersDetailView.as_view(), name='users-detail'),
    path('users/self/', views.SelfUserView.as_view(), name='user'),
    path('users/', views.UsersListView.as_view(), name='users-list'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('check-password/', views.CheckPasswordView.as_view(), name='check-password'),
    path('', include('drf_registration.urls')),
]
