from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer
from .models import Note
from .utils.logging_utility import (
    log_info, log_warning, log_error, log_debug, LogFunctionCall
)

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        with LogFunctionCall("NoteListCreate.get_queryset", self.request.user.id):
            try:
                queryset = Note.objects.select_related('author').all().order_by('-created_at')
                log_info(f"Retrieved {queryset.count()} notes for user {self.request.user.username}")
                return queryset
            except Exception as e:
                log_error("Failed to retrieve notes", e)
                raise
    
    def perform_create(self, serializer):
        with LogFunctionCall("NoteListCreate.perform_create", self.request.user.id):
            try:
                if serializer.is_valid():
                    note = serializer.save(author=self.request.user)
                    log_info(f"Note created successfully - ID: {note.id}, Title: '{note.title}', Author: {self.request.user.username}")
                else:
                    log_warning(f"Invalid note creation attempt by user {self.request.user.username}", 
                               {"errors": serializer.errors})
                    print(serializer.errors)
            except Exception as e:
                log_error(f"Error creating note for user {self.request.user.username}", e)
                raise

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        with LogFunctionCall("NoteDelete.get_queryset", self.request.user.id):
            try:
                if self.request.user.is_staff or self.request.user.is_superuser:
                    log_info(f"Admin user {self.request.user.username} accessing delete queryset")
                    return Note.objects.all()
                else:
                    log_warning(f"Non-admin user {self.request.user.username} attempted to access delete queryset")
                    return Note.objects.none()
            except Exception as e:
                log_error("Error in delete queryset", e)
                raise
    
    def destroy(self, request, *args, **kwargs):
        with LogFunctionCall("NoteDelete.destroy", request.user.id):
            try:
                if not (request.user.is_staff or request.user.is_superuser):
                    log_warning(f"Unauthorized delete attempt by user {request.user.username}")
                    return Response(
                        {"error": "Only administrators can delete notes"}, 
                        status=403
                    )
                
                # Get the note before deletion for logging
                note = self.get_object()
                note_info = {
                    "id": note.id,
                    "title": note.title,
                    "author": note.author.username
                }
                
                result = super().destroy(request, *args, **kwargs)
                log_info(f"Note deleted successfully by admin {request.user.username}", note_info)
                return result
                
            except Exception as e:
                log_error(f"Error deleting note for admin {request.user.username}", e)
                raise

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        with LogFunctionCall("CreateUserView.perform_create"):
            try:
                if serializer.is_valid():
                    user = serializer.save()
                    log_info(f"New user registered successfully - Username: {user.username}, ID: {user.id}")
                else:
                    log_warning("Invalid user registration attempt", {"errors": serializer.errors})
            except Exception as e:
                log_error("Error during user registration", e)
                raise

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        with LogFunctionCall("CurrentUserView.get", request.user.id):
            try:
                user_data = {
                    'id': request.user.id,
                    'username': request.user.username,
                    'is_admin': request.user.is_staff or request.user.is_superuser,
                    'is_staff': request.user.is_staff,
                    'is_superuser': request.user.is_superuser
                }
                log_debug(f"User info retrieved for {request.user.username}")
                return Response(user_data)
            except Exception as e:
                log_error(f"Error retrieving user info for {request.user.username}", e)
                raise