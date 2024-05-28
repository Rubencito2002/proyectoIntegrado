from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/user/', views.register_user, name='register_user'),
    path('success/', views.success, name='success'),
]