from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.db.models import Max




class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class StudentManager(models.Manager):
    def create(self, **kwargs):
        if 'student_id' not in kwargs:
            max_id = self.aggregate(max_id=Max('student_id'))['max_id']
            kwargs['student_id'] = 1 if max_id is None else max_id + 1
        else:
            raise ValueError('cannot directly assigen student id.')
        return super(StudentManager, self).create(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Student(models.Model):

    """Student object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    student_id = models.IntegerField(unique=True, db_column='StudentID')
    name = models.CharField(max_length=255, db_column='StudentName')
    id_number = models.CharField(max_length=10, blank=True, null=True, db_column='IDnum')
    address = models.CharField(max_length=100, blank=True, null=True, db_column='Address')
    city = models.CharField(max_length=50, blank=True, null=True, db_column='City')
    postal_code = models.CharField(max_length=6, blank=True, null=True, db_column='PostalCode')
    phone_number = models.CharField(max_length=30, blank=True, null=True, db_column='PhoneNumber')
    phone_number2 = models.CharField(max_length=50, blank=True, null=True, db_column='PhoneNumber2')
    fax_number = models.CharField(max_length=30, blank=True, null=True, db_column='FaxNumber')
    mobile_number = models.CharField(max_length=30, blank=True, null=True, db_column='MobileNumber')
    email_address = models.CharField(max_length=255, blank=True, null=True, db_column='EmailAddress')
    join_date = models.DateTimeField(blank=True, null=True, db_column='Joindate')
    birth_date = models.DateTimeField(blank=True, null=True, db_column='Bir_date')
    notes = models.TextField(max_length=2048, blank=True, null=True, db_column='Notes')
    firm_name = models.CharField(max_length=50, blank=True, null=True, db_column='FirmName')
    contact_person = models.CharField(max_length=50, blank=True, null=True, db_column='ContactPerson')
    division = models.CharField(max_length=50, blank=True, null=True, db_column='Devision')
    website = models.CharField(max_length=50, blank=True, null=True, db_column='website')
    credit_card = models.CharField(max_length=50, blank=True, null=True, db_column='CreditCard')
    maavar = models.BooleanField(default=False, db_column='maavar')
    credit_card_owner = models.CharField(max_length=50, blank=True, null=True, db_column='CrditCardOwner')
    credit_card_type = models.PositiveSmallIntegerField(blank=True, null=True, db_column='CrditCardType')
    valid = models.CharField(max_length=5, blank=True, null=True, db_column='Valid')
    mehiron_number = models.PositiveSmallIntegerField(blank=True, null=True, db_column='MehironNumber')
    id_card_owner = models.CharField(max_length=10, blank=True, null=True, db_column='idCardOwner')
    payment_terms = models.SmallIntegerField(blank=True, null=True, db_column='TnaiTashlum')
    discount_percentage = models.FloatField(blank=True, null=True, db_column='DiscountPR')
    photo_path = models.CharField(max_length=50, blank=True, null=True, db_column='PhotoPath')
    field_type_id = models.IntegerField(blank=True, null=True, db_column='fldTypeID')
    bank = models.IntegerField(blank=True, null=True, db_column='Bank')
    branch = models.IntegerField(blank=True, null=True, db_column='Branch')
    account = models.CharField(max_length=50, blank=True, null=True, db_column='Account')
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='OpeningBalance')
    opening_balance_date = models.DateTimeField(blank=True, null=True, db_column='OpeningBalancedate')
    no_vat = models.BooleanField(default=False, db_column='NoVat')
    seif_income = models.SmallIntegerField(blank=True, null=True, db_column='SeifIncome')
    lo_pail = models.BooleanField(default=False, db_column='LoPail')
    cust_type = models.PositiveSmallIntegerField(blank=True, null=True, db_column='CustType')
    cvv = models.SmallIntegerField(blank=True, null=True, db_column='CVV')

    objects = StudentManager()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Students' 
