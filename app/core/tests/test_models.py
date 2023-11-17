"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Student
from core import models
from django.core.exceptions import ValidationError



class UserModelTests(TestCase):
    """Test User models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


class StudentModelTest(TestCase):
    
    def test_create_student(self):
        """Test creating a student is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        student = models.Student.objects.create(
            user=user,
            name='Sample student name',
        )

        self.assertEqual(str(student), student.name)

    def test_student_id_auto_increment(self):
        # Create students using the custom manager method and check the auto-increment of student_id
        student1 = Student.objects.create(name="Student 1")
        self.assertEqual(student1.student_id, 1)

        student2 = Student.objects.create(name="Student 2")
        self.assertEqual(student2.student_id, 2)