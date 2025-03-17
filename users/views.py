from urllib import request
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from users.forms import AddPositionform, AddTaskforUser, AddTegform, AddUserForm, EditUserForm, RegistrationForm
from users.models import Tasks, UserProfile, UserStatus
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    users = UserProfile.objects.order_by("-score")
    context = {
        "users":users
    }
    return render(request,"index.html",context)
@login_required
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
            print(form.errors)  # Debug uchun xatoliklarni chop qilish
            return render(request, "add_user.html", {"form": form})  # Xatolik bilan formni qaytarish
@login_required
def delete_user(request,id):
    del_user = get_object_or_404(UserProfile,id=id)
    del_user.delete()
    return redirect('home')

@login_required
def user_status(request, id):
    user = get_object_or_404(UserProfile, id=id)
    
    # "Jarayonda" bo'lgan vazifalarni olish
    tasks = Tasks.objects.filter(user__id=id, status__name="Jarayonda")
    
    # "Jarayonda" bo'lmagan vazifalar
    done_task = Tasks.objects.filter(user__id=id).exclude(status__name="Jarayonda")
    
    # "Bajarilmadi" statusini olish
    bajarilmadi_status = UserStatus.objects.get(name="Bajarilmadi")

    # "Jarayonda" bo'lgan, ammo vaqt oralig'ida bo'lmaganlarni yangilash
    Tasks.objects.filter(
        user__id=id,
        status__name="Jarayonda"
    ).filter(~Q(start_time__lte=now(), end_time__gte=now())).update(status=bajarilmadi_status)

    print("Foydalanuvchi:", user.user.first_name)  # Debug ma'lumot
    
    context = {
        "tasks": tasks,
        "user": user,
        "donetasks": done_task
    }
    
    return render(request, "tasks.html", context)


@login_required
def update_task_status(request, task_id):
    if request.method != "POST":
        return redirect("home") 

    task = get_object_or_404(Tasks, id=task_id)
    new_status_name = request.POST.get("status")
    new_status = get_object_or_404(UserStatus, name=new_status_name)

    #agar status allaqachon ozgartirilgan bolsa
    if task.status.name != "Jarayonda":
        return redirect("user_status", id=task.user.id)

    #agar vaqt oraligida emas bolsa
    if not (task.start_time and task.end_time and task.start_time <= now() <= task.end_time):
        return redirect("user_status", id=task.user.id)

    if new_status.name == "Bajarildi":
        task.user.score += 10
        task.user.save()

    task.status = new_status
    task.save()

   
    return redirect("user_status", id=task.user.id)

@login_required
def add_task_for_user(request):
    if request.method == "GET":
        form = AddTaskforUser()
        return render(request,'add_task.html',{"form":form})
    elif request.method == "POST":
        form = AddTaskforUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
@login_required
def edit_user(request,id):
    user = get_object_or_404(UserProfile,id=id)
    if request.method == "GET":
        form = EditUserForm(instance=user)
        context = {
            "form":form,
            "user":user
        }
        return render(request,'edit_user.html',context)
    elif request.method == "POST":
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = {
            "form":form
        }
        return render(request,"login.html",context)
    elif request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
        else:
            context = {
                'form':form,
            }

            return render(request, 'login.html', context)
     
def register(request):
    if request.method == "POST":
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {
                'form':form,
            }
            print(form.errors)
            return render(request, 'register.html', context)
        # return redirect('register')
    else:

        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'register.html',context)
@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')



@login_required
def add_teg(request):
    if request.method == "GET":
        form = AddTegform()
        return render(request, 'add_teg.html', {"form": form})
    
    elif request.method == "POST":
        form = AddTegform(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print("Form errorrrrrr", form.errors)  

    return render(request, 'add_teg.html', {"form": form})  


@login_required
def add_position(request):
    if request.method == "GET":
        form = AddPositionform()
        return render(request, 'add_position.html', {"form": form})
    
    elif request.method == "POST":
        form = AddPositionform(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print("Form errorrrrrr", form.errors)  

    return render(request, 'add_position.html', {"form": form})  
