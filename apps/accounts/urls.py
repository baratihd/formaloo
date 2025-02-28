from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.accounts.views import SignupView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
]
