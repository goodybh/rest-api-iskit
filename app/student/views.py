"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Student
from student import serializers


class StudentViewSet(viewsets.ModelViewSet):
    """View for manage student APIs."""
    serializer_class = serializers.StudentSerializer
    queryset = Student.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve students for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-student_id')
    
    def perform_create(self, serializer):
        """Create a new student."""
        serializer.save(user=self.request.user)

