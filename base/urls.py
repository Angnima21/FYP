from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.auth_view, name='auth'),  # Combined login/registration
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),  # Add a home view if needed
]