from django import forms

# from core.constants import
from account.models import UserAccount
from campaign.models import Vaccine, DoseBooking, VaccineCampaign, Review


class VaccineForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={"name": "description", "rows": 3, "cols": 5})
    )

    class Meta:
        model = Vaccine
        fields = ["vaccine_name", "description", "dose_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-white "
                        "text-black border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )


class AddCampaignForm(forms.ModelForm):
    class Meta:
        model = VaccineCampaign
        fields = [
            "campaign_name",
            "image",
            "description",
            "start_date",
            "end_date",
            "place",
            "vaccine",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 "
                        "text-gray-700 border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )


#################################################################

from django import forms
from .models import DoseBooking


class DoseBookingForm(forms.ModelForm):
    class Meta:
        model = DoseBooking
        fields = ["first_dose_date", "campaign", "vaccine"]

    def __init__(self, *args, **kwargs):
        self.campaign = kwargs.pop("campaign", None)
        self.vaccine = kwargs.pop("vaccine", None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-white "
                        "text-black border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.campaign = self.campaign
        instance.vaccine = self.vaccine
        if commit:
            instance.save()
        return instance


# class DoseBookingForm(forms.ModelForm):
#   class Meta:
#     model = DoseBooking
#     fields = ["first_dose_date", "campaign"]

#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     for field in self.fields:
#       self.fields[field].widget.attrs.update(
#           {
#               "class": (
#                   "appearance-none block w-full bg-white "
#                   "text-black border border-gray-200 rounded "
#                   "py-3 px-4 leading-tight focus:outline-none "
#                   "focus:bg-white focus:border-gray-500"
#               )
#           }
#       )
# if 'campaign' in kwargs:
#   self.fields['campaign'].initial = kwargs.get('campaign')

# .......................................................................

# class DoseBookingForm(forms.ModelForm):
#     class Meta:
#         model = DoseBooking
#         fields = ["first_dose_date", "campaign"]

#     # def __init__(self, *args, **kwargs):
#     #     self.patient = kwargs.pop('patient') # account value ke pop kore anlam
#     #     super().__init__(*args, **kwargs)
#     #     self.fields['campaign'].disabled = True # ei field disable thakbe
#     #     self.fields['campaign'].widget = forms.HiddenInput() # user er theke hide kora thakbe

#     def __init__(self, *args, campaign=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['campaign'].widget = forms.HiddenInput()
#         if campaign:
#             self.fields['campaign'].initial = campaign


#############################################################################################


class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    body = forms.CharField(
        widget=forms.Textarea(attrs={"name": "body", "rows": 3, "cols": 5})
    )

    class Meta:
        model = Review
        fields = ["name", "email", "body", "rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.reviewer:
            # If the comment instance has a user associated with it, prepopulate name and email
            # Assuming you have a user field in Comment model
            self.fields["name"].initial = self.instance.reviewer.get_full_name()
            # self.fields['name'].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.reviewer

        elif self.instance and not self.instance.reviewer:
            # If the comment instance doesn't have a user, prepopulate with current user (if authenticated)
            user=self.initial.get("reviewer")
            if user and user.is_authenticated:
                # self.fields['name'].initial = user.username
                self.fields["name"].initial=user.get_full_name()
                self.fields["email"].initial=user.email



