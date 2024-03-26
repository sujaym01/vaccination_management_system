from django.shortcuts import render
from contact_us.forms import ContactForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
class UserContactCreateView(FormView):
    template_name = "contact_us/contact_us_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        messages.success(self.request, "Welcome!!")
        return super().form_valid(form)
