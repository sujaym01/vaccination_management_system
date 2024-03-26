from django.urls import path
from .views import (
    VaccineCreateView,
    VaccineListView,
    VaccineUpdateView,
    VaccineDeleteView,
    DoseBookingCreateView,
    AddCampaignCreateView,
    CampaignDetailView,all_campaign
)

urlpatterns = [
    path("add_campaign/", AddCampaignCreateView.as_view(), name="add_campaign"),
    path("all_campaign/", all_campaign, name="all_campaign"),
    path("add_vaccine/", VaccineCreateView.as_view(), name="add_vaccine"),
    path("vaccine_list/", VaccineListView.as_view(), name="vaccine_list"),
    path("vaccine/<int:pk>/edit/", VaccineUpdateView.as_view(), name="edit_vaccine"),
    path(
        "vaccine/<int:pk>/delete/", VaccineDeleteView.as_view(), name="delete_vaccine"
    ),
    path("details/<int:id>/", CampaignDetailView.as_view(), name="campaign_detail"),
    path(
        "details/<int:campaign_id>/vaccine_booking/<int:vaccine_id>/",
        DoseBookingCreateView.as_view(),
        name="vaccine_booking",
    ),
]
