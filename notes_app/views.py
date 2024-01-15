from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import (
    viewsets,
    generics,
    permissions,
    status,
    response,
)
from .models import Note
from .serializers import (
    NoteAPISerializer,
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
        return Note.objects.filter(user=self.request.user)


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
