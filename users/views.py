from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from users.forms import AddTaskforUser, AddUserForm, EditUserForm
from users.models import Tasks, UserStatus, Users
from django.contrib import messages

# Create your views here.
def home(request):
    users = Users.objects.order_by("-score")
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

def user_status(request,id):
    # user_status = get_object_or_404(Tasks,user__id=id)
    # return render(request,"tasks.html",{"status":user_status})
    user = get_object_or_404(Users,id=id)
    tasks = Tasks.objects.filter(user__id=id,status__name = "Jarayonda")
    done_task = Tasks.objects.filter(user__id=id).exclude(status__name = "Jarayonda")
    # print(done_task,"00000000000000000000000")
    context = {
        "tasks":tasks,
        "user":user,
        "donetasks":done_task
    }
    print(user,"0000000000000000000000000000000000000000000000")
    return render(request, "tasks.html", context)



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

def edit_user(request,id):
    user = get_object_or_404(Users,id=id)
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