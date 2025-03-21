from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Position, Tasks, Teg, UserProfile  # Modelni import qilish kerak

class AddUserForm(UserCreationForm):
    score = forms.IntegerField(initial=0, required=False)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),  # Mavjud bo'lgan barcha positionlarni olish
        required=True
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'score' in self.fields:
            del self.fields['score']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Default True
        user.is_staff = True  
        user.is_active = True  
        if commit:
            user.save()
            UserProfile.objects.create(user=user, score= 0,position=self.cleaned_data.get('position') )
        return user

class EditUserForm(forms.ModelForm):
    score = forms.IntegerField(initial=0,required=False)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),  # Mavjud bo'lgan barcha positionlarni olish
        required=True
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name' )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'score' in self.fields:
            del self.fields['score']
    def save(self, commit=True):
        user = super().save(commit=False)
        # Default True
        user.is_staff = True  
        user.is_active = True  
        if commit:
            user.save()
            UserProfile.objects.create(user=user, score= 0,position=self.cleaned_data.get('position') )
        return user
    
class AddTaskforUser(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["name",'description','user','start_time','end_time',"teg"]




class RegistrationForm(UserCreationForm):
    usable_password = None
    class Meta:
        model = User
        fields = ['username', 'email']
      

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Parollar mos emas.")
        return password2
    

class AddTegform(forms.ModelForm):
    class Meta:
        model = Teg
        fields = ["name"]

class AddPositionform(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]