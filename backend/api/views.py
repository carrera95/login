from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer
from .models import Note
# Add this import at the top
from rest_framework.views import APIView

# Add this class to your views.py
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'is_admin': request.user.is_staff or request.user.is_superuser,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser
        })

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show all notes to everyone (both admin and regular users)
        return Note.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only allow admins to delete any note
        # Regular users cannot delete any notes
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Note.objects.all()
        else:
            # Return empty queryset for non-admin users
            return Note.objects.none()
    
    def destroy(self, request, *args, **kwargs):
        # Additional check to ensure only admins can delete
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only administrators can delete notes"}, 
                status=403
            )
        return super().destroy(request, *args, **kwargs)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]