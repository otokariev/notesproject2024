from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NoteAPIViewSet,
    NoteAPICategoryViewSet,
    SearchAPIView,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserProfileAPIView,
)

router = DefaultRouter()
router.register(r'notes', NoteAPIViewSet, basename='notes')
router.register(r'categories', NoteAPICategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('search/', SearchAPIView.as_view(), name='search'),
]
