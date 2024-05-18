from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Class for creating the results view
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login") #Code to redirect the user to the login page after successful sign up
    template_name = "registration/signup.html"