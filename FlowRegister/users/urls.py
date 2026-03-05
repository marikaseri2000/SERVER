from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Registrazione (studente crea account)
    path('registra/', views.register_user, name='register_user'),
    
    path('info/', views.get_user_profile, name='get_user_profile'),
    
    # Login: Restituisce Access Token e Refresh Token
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Refresh: Se il token scade, ne chiedi uno nuovo qui
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]