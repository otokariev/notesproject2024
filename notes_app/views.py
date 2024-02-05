from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.pagination import PageNumberPagination
from rest_framework import (
    viewsets,
    generics,
    permissions,
    status,
    response,
    filters,
)
from .models import Note, NoteCategory
from .serializers import (
    NoteAPISerializer,
    NoteAPICategorySerializer,
    RegisterAPISerializer,
    LoginAPISerializer,
    UserProfileAPISerializer,
)


class NoteAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteAPISerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset


class NoteAPICategoryViewSet(viewsets.ModelViewSet):
    queryset = NoteCategory.objects.all()
    serializer_class = NoteAPICategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchAPIView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteAPISerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = RegisterAPISerializer


class LoginAPIView(generics.CreateAPIView):
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = LoginAPISerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return response.Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return response.Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return response.Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserProfileAPISerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        super(UserProfileAPIView, self).perform_update(serializer)
