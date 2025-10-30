from django.db import models

class UserOTP(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
