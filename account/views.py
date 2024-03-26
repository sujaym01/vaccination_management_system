from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from .models import UserAccount
from django.views.generic import RedirectView, FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from campaign.models import DoseBooking, Vaccine


# Create your views here.

def send_password_change_email(user, subject, template):
    message = render_to_string(template, {
        'user': user,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()
    


class UserRegistrationView(FormView):
    template_name = "account/user_registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # print(form.cleaned_data)
        # user = form.save(commit=False)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Your registration has been successfully!")
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     print(form.errors)
    #     print(form.cleaned_data)
    #     return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = "account/user_login.html"

    def get_success_url(self):
        return reverse_lazy("home")
        # return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Login Successfully, Welcome Back!!")
        return super().form_valid(form)


class UserLogoutView(RedirectView):
    url = reverse_lazy("home")  # Redirect to home after logout

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            messages.warning(self.request, "Logout Successfully!!")
        return super().get(request, *args, **kwargs)


# class UserLogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('home')

# class UserLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         logout(self.request)
#         messages.warning(self.request, "Logout Successfully!!")
#         return HttpResponseRedirect(reverse_lazy('home'))


# class UserAccountUpdateView(View):
#     template_name = "profile.html"

#     def get(self, request):
#         form = UserUpdateForm(instance=request.user)
#         return render(request, self.template_name, {"form": form})

#     def post(self, request):
#         form = UserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("profile")
#         return render(request, self.template_name, {"form": form})


class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = "account/user_update_profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("update_profile")  # Redirect to the user's profile page
        return render(request, self.template_name, {"form": form})


# class PasswordChangeView(LoginRequiredMixin, FormView):
#     template_name = "password_change.html"
#     form_class = StyledPasswordChangeForm
#     success_url = reverse_lazy("profile")

#     def form_valid(self, form):
#         form.save()
#         update_session_auth_hash(self.request, form.user)
#         messages.success(self.request, "Change Password Successfully!! Thank You!!")
#         return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["user"] = self.request.user

#         return kwargs


class UserPasswordChangeView(PasswordChangeView):
    template_name = "account/password_change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("profile")
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password was successfully updated!")
        update_session_auth_hash(self.request, form.user)
        
        send_password_change_email(
            self.request.user,
            "Password Changed",
            "account/password_change_mail.html"
        )
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, View):
    template_name = "account/user_profile.html"

    def get(self, request):
        user_details = UserAccount.objects.filter(user=request.user).first()
        # print(user_details.country, user_details.account_type)

        # user_address = UserAccount.objects.filter(user_id=request.user)
        # for i in user_address:
        #     print(i.country, i.user, i.city, i.street_address,i.postal_code, i.image)

        if self.request.user.account.account_type == "Patient":
            vaccine_details = DoseBooking.objects.filter(patient=request.user)
            # print(vaccine_details.first_dose_date,vaccine_details.is_completed,vaccine_details.second_dose_date)
            return render(
                request, self.template_name, {"vaccine_details": vaccine_details}
            )

        # if self.request.user.account.account_type == "Doctor":
        #     user = request.user.account
        #     vaccine_list = Vaccine.objects.filter(user_account=user).first()
        # print(vaccine_list)
        return render(request, self.template_name, {"user_details": user_details})
