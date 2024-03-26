from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount
from core.constants import ACCOUNT_TYPE, GENDER_TYPES
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    nid_number = forms.CharField(max_length=17)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender = forms.ChoiceField(choices=GENDER_TYPES)
    postal_code = forms.IntegerField()
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=50)
    image = forms.ImageField()
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.EmailField(required=True)

    # first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))

    class Meta:
        model = User

        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "nid_number",
            "account_type",
            "date_of_birth",
            "gender",
            "postal_code",
            "street_address",
            "city",
            "country",
            "image",
        ]

    def clean(self):
        email = self.cleaned_data.get("email")
        nid_number = self.cleaned_data.get("nid_number")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        if UserAccount.objects.filter(nid_number=nid_number).exists():
            raise ValidationError("NID Number already exists")
        return self.cleaned_data

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            nid_number = self.cleaned_data.get("nid_number")
            account_type = self.cleaned_data.get("account_type")
            date_of_birth = self.cleaned_data.get("date_of_birth")
            gender = self.cleaned_data.get("gender")
            postal_code = self.cleaned_data.get("postal_code")
            street_address = self.cleaned_data.get("street_address")
            city = self.cleaned_data.get("city")
            country = self.cleaned_data.get("country")
            image = self.cleaned_data.get("image")

            UserAccount.objects.create(
                user=our_user,
                nid_number=nid_number,
                account_type=account_type,
                date_of_birth=date_of_birth,
                gender=gender,
                postal_code=postal_code,
                street_address=street_address,
                city=city,
                country=country,
                image=image,
            )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-white"
                        "text-black border border-gray-200 rounded "
                        "py-3 px-4 leading-tight focus:outline-none "
                        "focus:bg-white focus:border-gray-500"
                    )
                }
            )


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         model._meta.get_field('email')._unique = True
#         fields = ("username", "email", "password1", "password2")

############################################################################################


class UserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPES)
    postal_code = forms.IntegerField()
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    # image = forms.ImageField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

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
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None

            if user_account:
                self.fields["date_of_birth"].initial = user_account.date_of_birth
                self.fields["gender"].initial = user_account.gender
                self.fields["postal_code"].initial = user_account.postal_code
                self.fields["street_address"].initial = user_account.street_address
                self.fields["city"].initial = user_account.city
                self.fields["country"].initial = user_account.country
                # self.fields["image"].initial = user_account.image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.date_of_birth = self.cleaned_data["date_of_birth"]
            user_account.gender = self.cleaned_data["gender"]
            user_account.street_address = self.cleaned_data["street_address"]
            user_account.postal_code = self.cleaned_data["postal_code"]
            user_account.city = self.cleaned_data["city"]
            user_account.country = self.cleaned_data["country"]
            # user_account.image = self.cleaned_data["image"]
            user_account.save()

        return user


#######################################################################################
class PasswordChangeForm(PasswordChangeForm):
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
