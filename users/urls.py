from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    # Registration
    path('register/', views.register, name='register'),
    
    # Login/Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
