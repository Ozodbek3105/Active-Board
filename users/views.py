from django.shortcuts import get_object_or_404, redirect, render

from users.forms import AddUserForm
from users.models import Users

# Create your views here.
def home(request):
    users = Users.objects.all()
    context = {
        "users":users
    }
    return render(request,"index.html",context)

def add_user(request):
    if request.method == "GET":
        form = AddUserForm()
        return render(request,'add_user.html',{"form":form})
    
    elif request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)

def delete_user(request,id):
    del_user = get_object_or_404(Users,id=id)
    del_user.delete()
    return redirect('home')