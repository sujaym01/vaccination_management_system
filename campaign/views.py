from django.shortcuts import render
from .forms import VaccineForm, DoseBookingForm, AddCampaignForm, CommentForm
from datetime import datetime, timedelta
from .models import Vaccine, DoseBooking, VaccineCampaign
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    View,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.


class VaccineCreateView(CreateView):
    model = Vaccine
    form_class = VaccineForm
    template_name = "campaign/add_vaccine.html"
    success_url = reverse_lazy("vaccine_list")

    def form_valid(self, form):
        form.instance.user_account = self.request.user.account
        messages.success(self.request, "Vaccine Created Successfully!")
        return super().form_valid(form)


# class VaccineListView(ListView):
#     model = Vaccine
#     template_name = "campaign/vaccine_list.html"
#     context_object_name = "vaccine_list"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


from django.views.generic import ListView
from .models import Vaccine


class VaccineListView(ListView):
    model = Vaccine
    template_name = "campaign/vaccine_list.html"
    context_object_name = "vaccine_list"

    def get_queryset(self):
        # Assuming you're using User model with a related Account model
        user_account = self.request.user.account
        return Vaccine.objects.filter(user_account=user_account)


class VaccineUpdateView(UpdateView):
    model = Vaccine
    form_class = VaccineForm
    template_name = "campaign/update_vaccine.html"
    success_url = reverse_lazy("vaccine_list")


class VaccineDeleteView(DeleteView):
    model = Vaccine
    template_name = "campaign/vaccine_confirm_delete.html"
    success_url = reverse_lazy("vaccine_list")


class AddCampaignCreateView(CreateView):
    model = VaccineCampaign
    form_class = AddCampaignForm
    template_name = "campaign/add_campaign.html"
    success_url = reverse_lazy("add_campaign")

    def form_valid(self, form):
        form.instance.campaigner = self.request.user.account
        messages.success(self.request, "Campaign Added Successfully!")
        return super().form_valid(form)


# <<<<<<<<<<<<<<<<<<<<< DoseBookingCreateView >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class DoseBookingCreateView(LoginRequiredMixin, CreateView):
    model = DoseBooking
    form_class = DoseBookingForm
    template_name = "campaign/dose_booking.html"
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        campaign_id = self.kwargs.get("campaign_id")
        campaign = get_object_or_404(VaccineCampaign, pk=campaign_id)
        vaccine = get_object_or_404(Vaccine, pk=campaign_id)
        # print(vaccine.vaccine_name)
        kwargs["campaign"] = campaign
        kwargs["vaccine"] = vaccine
        return kwargs

    def form_valid(self, form):
        form.instance.patient = self.request.user
        form.instance.second_dose_date = (
            form.instance.first_dose_date.schedule + timedelta(days=21)
        )
        form.save()
        messages.success(self.request, "First Dose Booking Successfully!! Thank You!!")
        return super().form_valid(form)

    # def form_valid(self, form):
    #     try:
    #         form.instance.patient = self.request.user
    #         form.instance.second_dose_date = form.instance.first_dose_date.schedule + timedelta(days=21)
    #         form.save()
    #         messages.success(self.request, " First Dose Booking Successfully!! Thank You!!")
    #         return super().form_valid(form)
    #     except IntegrityError:
    #         messages.error(self.request, f"Dose booking for {self.request.user} already exists.")
    #         return self.form_invalid(form)

    # def form_invalid(self, form):
    #     messages.error(self.request, f"Dose booking for {self.request.user} already exists.")
    #     return super().form_invalid(form)


###################################################################################

# class DoseBookingCreateView(LoginRequiredMixin, CreateView):
#     model = DoseBooking
#     form_class = DoseBookingForm
#     template_name = "campaign/dose_booking.html"
#     success_url = reverse_lazy("home")

#     def form_valid(self, form):
#         form.instance.patient = self.request.user
#         form.instance.second_dose_date = form.instance.first_dose_date.schedule + timedelta(days=21)
#         messages.success(self.request, "Dose Booking Successfully!! Thank You!!")
#         return super().form_valid(form)


# class DoseBookingCreateView1(LoginRequiredMixin, CreateView):
#     model = DoseBooking
#     form_class = DoseBookingForm
#     template_name = "campaign/dose_booking.html"
#     success_url = reverse_lazy("home")
#     campaign = None  # Initialize campaign attribute

# def get(self, request, campaign_id, vaccine_id):
#     self.campaign = get_object_or_404(VaccineCampaign, pk=campaign_id)  # Set campaign here
#     self.vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
#     return super().get(request, campaign_id, vaccine_id)

# def get(self, request, campaign_id, vaccine_id):
#     self.campaign = get_object_or_404(VaccineCampaign, pk=campaign_id)
#     self.vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
#     form = self.form_class(campaign=self.campaign)  # Pass campaign object to the form
# Now you have campaign and vaccine objects, you can use them as needed
#     return self.render_to_response({'form': form, 'campaign': self.campaign, 'vaccine': self.vaccine})

# def form_valid(self, form):
#     try:
#         form.instance.campaign = self.campaign
#         print("line 199 " ,form.instance.campaign)
#         form.instance.patient = self.request.user
#         form.instance.second_dose_date = form.instance.first_dose_date.schedule + timedelta(days=21)
#         form.save()
#         messages.success(self.request, "First Dose Booking Successfully!! Thank You!!")
#         return super().form_valid(form)
#     except IntegrityError:
#         messages.error(self.request, f"Dose booking for {self.request.user} already exists.")
#         return self.form_invalid(form)


# <<<<<<<<<<<<<<<<<<<<<<CampaignDetailView >>>>>>>>>>>>>>>>>>>>>>>>>>>>


class CampaignDetailView(DetailView):
    model = VaccineCampaign
    pk_url_kwarg = "id"
    template_name = "campaign/campaign_details.html"
    context_object_name = "campaign"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        campaign = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.campaign = campaign
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.object
        comments = campaign.reviews.all()
        user = self.request.user

        # comment_form = CommentForm()
        comment_form = CommentForm(initial={'reviewer': user})
        # Check if the user has booked a service for this campaign
        user = self.request.user
        if user.is_authenticated:
            dose_booking_exists = DoseBooking.objects.filter(
                patient=user, campaign=campaign
            ).exists()
            context["can_leave_review"] = dose_booking_exists
        else:
            context["can_leave_review"] = False

        context["comments"] = comments
        context["comment_form"] = comment_form
        return context



# class CampaignDetailView(DetailView):
#     model = VaccineCampaign
#     pk_url_kwarg = 'id'
#     template_name = 'campaign/campaign_details.html'
#     context_object_name='campaign'

# class CampaignDetailView(View):
#     template_name = 'campaign/campaign_details.html'
#     def get(self, request, *args, **kwargs):
#         campaign = get_object_or_404(VaccineCampaign, pk=kwargs['id'])
#         # print(campaign.campaigner)
#         context = {'campaign': campaign}
#         return render(request, self.template_name, context)


def all_campaign(request):
    campaign = VaccineCampaign.objects.all().order_by("-campaign_name")
    return render(request, "campaign/campaign.html", {"all_campaign": campaign})
