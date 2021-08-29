from django.urls import path

from .views import CustomUserCreate, UserDetailView, BlacklistTokenUpdateView, TestUserDetailView , LoginAPI


urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='user-register'),
    path('detail/', UserDetailView.as_view(), name='user-detail'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('test/', TestUserDetailView.as_view(), name='test'),
    path('logintest/', LoginAPI.as_view(), name='test2'),
]
