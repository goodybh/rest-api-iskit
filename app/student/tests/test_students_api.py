
"""
Tests for student APIs.
"""
from datetime import datetime, timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Student

from student.serializers import StudentSerializer

def detail_url(student_id):
    """Create and return a student detail URL."""
    return reverse('student:student-detail', args=[student_id])

STUDENTS_URL = reverse('student:student-list')


def create_student(user,name, **params):
    student = Student.objects.create(user=user, name = name, **params)
    return student


class PublicStudentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(STUDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_students(self):
        """Test retrieving a list of students."""
        create_student(user=self.user, name = 'user1')
        create_student(user=self.user, name = 'user2')

        res = self.client.get(STUDENTS_URL)

        students = Student.objects.all().order_by('-student_id')
        serializer = StudentSerializer(students, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_student_list_for_all_users(self):
        """Test list of students contains students for all users."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_student(user=other_user, name='user1')
        create_student(user=self.user, name='user2')

        res = self.client.get(STUDENTS_URL)

        # Fetch all students and order them by a consistent field, e.g., 'student_id'
        students = Student.objects.all().order_by('student_id')
        serializer = StudentSerializer(students, many=True)

        # Also sort the response data by the same field
        res_data_sorted = sorted(res.data, key=lambda x: x['student_id'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data_sorted, serializer.data)

    def test_create_student(self):
        """Test creating a student."""
        payload = {
            'name': 'Sample student',
        }
        res = self.client.post(STUDENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(student_id=res.data['student_id'])
        for k, v in payload.items():
            self.assertEqual(getattr(student, k), v)
        self.assertEqual(student.user, self.user)
    
    def test_student_id_assignment(self):
        """Test that student IDs are assigned correctly."""
        student1 = create_student(user=self.user, name='Student 1')
        student2 = create_student(user=self.user, name='Student 2')

        self.assertEqual(student2.student_id, student1.student_id + 1)
    
    def test_create_student_invalid(self):
        """Test creating a student with invalid payload."""
        payload = {'name': ''}  # Missing or invalid data
        res = self.client.post(STUDENTS_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_create_student_complex(self):
        """Test creating a student with complex payload."""
        payload = {
            "name": "hello hello 1234",
            "id_number": "string",
            "address": "string",
            "city": "string",
            "postal_code": "string",
            "phone_number": "string",
            "phone_number2": "string",
            "fax_number": "string",
            "mobile_number": "string",
            "email_address": "string",
            "notes": "string",
            "firm_name": "string",
            "contact_person": "string",
            "division": "string",
            "website": "string",
            "credit_card": "string",
            "maavar": True,
            "credit_card_owner": "string",
            "credit_card_type": 255,
            "valid": "strin",
            "id_card_owner": "string",
            "discount_percentage": 0,
            "photo_path": "string",
            "field_type_id": 2147483647,
            "bank": 2147483647,
            "branch": 2147483647,
            "account": "string",
            "opening_balance": 0,
            "opening_balance_date": datetime.fromisoformat('2023-11-19T13:26:05.471+00:00').astimezone(timezone.utc),
            "cust_type": 235,
            "cvv": 255
        }   
        res = self.client.post(STUDENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(student_id=res.data['student_id'])
        for k, v in payload.items():
            self.assertEqual(getattr(student, k), v)
        self.assertEqual(student.user, self.user)
