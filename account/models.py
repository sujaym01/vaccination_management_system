from django.db import models
from datetime import date
from django.contrib.auth.models import User
from core.constants import ACCOUNT_TYPE, GENDER_TYPES

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    nid_number = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="NID Number",
        help_text="<em>10 / 13 / 17</em> digits format",
    )
    date_of_birth = models.DateField(
        help_text="Please use the following format: <em>YYYY-MM-DD</em>."
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE,
        help_text="<em>Choice Your role Patient or Doctor</em>",
    )
    image = models.ImageField(upload_to="account/media/images/")
    gender = models.CharField(max_length=10, choices=GENDER_TYPES)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=50)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            delta_in_years = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
            return delta_in_years
        return None

    def __str__(self):
        return f"{self.account_type} :  {self.user.username}"
