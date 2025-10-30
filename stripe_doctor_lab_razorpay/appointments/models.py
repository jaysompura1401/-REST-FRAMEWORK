from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    fee = models.IntegerField(help_text='Fee in INR (e.g., 500)')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} ({self.appointment_date})"
