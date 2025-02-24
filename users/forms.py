from django import forms
from .models import Users  # Modelni import qilish kerak

class AddUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'score', 'position']
