from django.urls import path
from .views import UserContactCreateView

urlpatterns = [
    path("contact_us/", UserContactCreateView.as_view(), name="contact_us"),
]
