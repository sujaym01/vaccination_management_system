from django.contrib import admin
from .models import VaccineSchedule,Vaccine,VaccineCampaign,DoseBooking,Review
# Register your models here.
admin.site.register(VaccineSchedule)
admin.site.register(Vaccine)
admin.site.register(VaccineCampaign)
admin.site.register(DoseBooking)
admin.site.register(Review)

