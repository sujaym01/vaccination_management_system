from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"
