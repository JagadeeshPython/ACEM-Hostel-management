from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User

class Room(models.Model):
    
    room_number = models.CharField(
        max_length=10,
        unique=True
    )

    capacity = models.IntegerField(
        default=4
    )

    def __str__(self):
        return self.room_number

class Student(models.Model):
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(max_length=15)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    address = models.TextField()

    room = models.ForeignKey(
    Room,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    rent_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=3000.00
    )

    rent_status = models.BooleanField(
        default=False
    )

    photo = models.ImageField(
        upload_to='student_photos/',
        blank=True,
        null=True
    )

    parent_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    parent_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    parent_email = models.EmailField(
        blank=True,
        null=True
    )

    join_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} ({self.room.room_number if self.room else 'No Room'})"

class Complaint(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)

    msg = models.TextField()

    date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    response = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

class RentPaymentHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    month = models.CharField(
        max_length=20
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    amount_paid = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    remaining_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    date_paid = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=[
            ('paid', 'paid'),
            ('unpaid', 'unpaid')
        ]
    )

    def __str__(self):
        return f"{self.student.name} |-| {self.date_paid} |-| {self.status}"


class Contact(models.Model):

    name = models.CharField(
        max_length=50
    )

    mobile_number = models.CharField(
        max_length=10
    )

    visitor_email = models.EmailField()

    msg = models.TextField(
        blank=True,
        null=True
    )

    contact_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} |-| {self.contact_date} |-| {self.visitor_email} |-| {self.mobile_number}"


class Payment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    month = models.CharField(
        max_length=20
    )

    amount_paid = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.month}"


class Attendance(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    MORNING = 'Morning'
    EVENING = 'Evening'
    NIGHT = 'Night'

    SESSION_CHOICES = [
        (MORNING, 'Morning'),
        (EVENING, 'Evening'),
        (NIGHT, 'Night'),
    ]

    session = models.CharField(
        max_length=20,
        choices=SESSION_CHOICES
    )

    date = models.DateField(
        default=timezone.now
    )

    marked_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default='Present'
    )

    class Meta:
        unique_together = (
            'student',
            'session',
            'date'
        )

    def __str__(self):
        return f"{self.student.username} - {self.session}"


# ==========================
# LEAVE REQUEST MODULE
# ==========================

class LeaveRequest(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    from_date = models.DateField()

    to_date = models.DateField()

    reason = models.TextField()

    applied_on = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    approved_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return (
            f"{self.student.name} | "
            f"{self.from_date} to {self.to_date} | "
            f"{self.status}"
        )
        

class HostelIncharge(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    gender = models.CharField(
        max_length=10
    )

    address = models.TextField()

    designation = models.CharField(
        max_length=100,
        default="Hostel Incharge"
    )

    joining_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    

from django.db import models
from django.utils import timezone
import uuid

class Outpass(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Used', 'Used'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    outpass_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    destination = models.CharField(
        max_length=200
    )

    reason = models.TextField()

    out_time = models.DateTimeField()

    return_time = models.DateTimeField()

    emergency_contact = models.CharField(
        max_length=15
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    approved_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    applied_on = models.DateTimeField(
        auto_now_add=True
    )

    approved_on = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.outpass_id:
            self.outpass_id = (
                "OP" +
                timezone.now().strftime("%Y%m%d%H%M%S")
            )

        super().save(*args, **kwargs)

    @property
    def permission_hours(self):

        diff = self.return_time - self.out_time

        return round(
            diff.total_seconds() / 3600,
            2
        )

    def __str__(self):
        return self.outpass_id
    

class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('national', 'National Holiday'),
        ('festival', 'Festival Holiday'),
        ('hostel', 'Hostel Holiday'),
        ('emergency', 'Emergency Holiday'),
    ]

    title = models.CharField(max_length=200)
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)


class AttendanceNotification(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date}"

