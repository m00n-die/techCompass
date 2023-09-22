from django.forms import ModelForm
from .models import Job
from django.contrib.auth.models import User


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        exclude = ['posted_by']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', ]