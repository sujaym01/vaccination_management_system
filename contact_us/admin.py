from django.contrib import admin

# Register your models here.
from django.contrib import admin
from contact_us.models import ContactUs
# admin.site.register(ContactUs)
from django import forms
from contact_us.forms import ContactForm
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

# class ContactForm(forms.ModelForm):
#     class Meta:
#         widgets = {                          
#             'phone': PhoneNumberPrefixWidget(initial='US'),
#         }

@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm