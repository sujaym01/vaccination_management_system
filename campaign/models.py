from django.db import models
from django.contrib.auth.models import User
from account.models import UserAccount
from core.constants import VACCINE_NAME, PLACE_CHOICES, STAR_CHOICES

# Create your models here.


class VaccineSchedule(models.Model):
    doctor = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, blank=True, null=True
    )
    schedule = models.DateTimeField()

    def __str__(self):
        return str(self.schedule)


class Vaccine(models.Model):
    vaccine_name = models.CharField(max_length=20, choices=VACCINE_NAME)
    description = models.TextField()
    dose_number = models.IntegerField(default=1)
    # available_date = models.ManyToManyField(VaccineSchedule)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.vaccine_name


class VaccineCampaign(models.Model):
    campaigner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="campaign/media/images/", blank=True, null=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    place = models.CharField(max_length=100, choices=PLACE_CHOICES)
    vaccine = models.ManyToManyField(Vaccine)

    def __str__(self):
        return self.campaign_name


class DoseBooking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE, blank=True, null=True
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, blank=True, null=True
    )
    first_dose_date = models.ForeignKey(VaccineSchedule, on_delete=models.CASCADE)
    second_dose_date = models.DateField(default=None, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'{self.is_completed} - {self.first_dose_date}'
    def __str__(self):
        return f"Dose Booking for {self.patient} in Campaign {self.campaign}"


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE, related_name="reviews"
    )
    # dose_booking = models.ForeignKey(DoseBooking, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=STAR_CHOICES, max_length=10)

    class Meta:
        ordering = ["created_on"]

    # def save(self, *args, **kwargs):
    #     if self.dose_booking is None or self.dose_booking.campaign != self.campaign:
    #         raise ValueError("Reviewer must have a dose booking for the corresponding campaign to leave a review.")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return "Review for {} by {}".format(self.campaign, self.name)

    # def __str__(self):
    #     return 'Comment {} by {}'.format(self.body, self.name)

    # def __str__(self):
    #     return f"Reviewer: {self.reviwer.first_name}; Campaign: {self.campaign.campaign_name}"
