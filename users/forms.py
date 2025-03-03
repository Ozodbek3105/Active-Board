from django import forms
from .models import Tasks, Users  # Modelni import qilish kerak

class AddUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'score', 'position']


class AddTaskforUser(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = "__all__"


class EditUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'score', 'position']
