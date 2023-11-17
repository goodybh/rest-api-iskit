"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for students."""

    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'id_number', 'address', 'city', 'postal_code',
            'phone_number', 'phone_number2', 'fax_number', 'mobile_number', 'email_address',
            'join_date', 'birth_date', 'notes', 'firm_name', 'contact_person', 'division',
            'website', 'credit_card', 'maavar', 'credit_card_owner', 'credit_card_type',
            'valid', 'mehiron_number', 'id_card_owner', 'payment_terms', 'discount_percentage',
            'photo_path', 'field_type_id', 'bank', 'branch', 'account', 'opening_balance',
            'opening_balance_date', 'no_vat', 'seif_income', 'lo_pail', 'cust_type', 'cvv'
        ]
        read_only_fields = ['student_id']