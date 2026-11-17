# patients/models.py
from django.db import models


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    patient_id   = models.CharField(max_length=10, unique=True, editable=False)
    name         = models.CharField(max_length=100)
    age          = models.IntegerField()
    gender       = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address      = models.TextField()
    phone_number = models.CharField(max_length=15)
    email        = models.EmailField(unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by('-id').first()
            next_num = 1 if not last else last.id + 1
            self.patient_id = f"PAT-{next_num:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.patient_id
    
class Payment(models.Model):
    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Payment {self.transaction_id or 'N/A'} for {self.patient_name}"