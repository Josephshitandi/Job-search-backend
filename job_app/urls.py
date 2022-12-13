from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# user_profile = ProfileAPI.as_view({
#     'get': 'list',
#     'post': 'create'
# })


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('auth/signup/', SignupAPIView.as_view(), name='user_signup'),
    path('profile1/', views.ProfileList.as_view(),name='profiles'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',views.LogoutAPIView.as_view(),name='logout'),
    path('', include(router.urls)),
    path('jobs/', views.JobsViewSet.as_view()),

]