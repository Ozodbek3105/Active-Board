from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from users.forms import AddUserForm
from users.models import Tasks, UserStatus, Users

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

    tasks = Tasks.objects.filter(user__id=id)
    if not tasks:
        return HttpResponse(f"UserStatus with ID {id} not found", status=404)
    
    return render(request, "tasks.html", {"tasks": tasks})



# def update_task_status(request, task_id):
    # if request.method == "POST":
    #     new_status = request.POST.get("status")
    #     task = get_object_or_404(Tasks, id=task_id)
    #     current_time = now()

    #     # Faqat start_time va end_time oralig'ida o'zgartirish mumkin
    #     if not (task.start_time <= current_time <= task.end_time):
    #         return redirect("user_status", id=task_id)  # Xatolik bo‘lsa ham sahifaga qaytaramiz

    #     # Statusni yangilash
    #     task.status = new_status
    #     task.save()

    #     return redirect("user_status", id=task_id)  # Yangilangan sahifani yuklaymiz

    # return redirect("home")  # Agar noto‘g‘ri so‘rov bo‘lsa, bosh sahifaga yo‘naltiramiz

def update_task_status(request, task_id):
    if request.method == "POST":
        new_status_name = request.POST.get("status")
        task = get_object_or_404(Tasks, id=task_id)
        current_time = now()

        #Faqat start_time va end_time oralig‘ida o‘zgartiramiz
        if not (task.start_time <= current_time <= task.end_time) :
            return redirect("user_status", id=task_id)

        # UserStatus obyekti bazadan olindi
        new_status = get_object_or_404(UserStatus, name=new_status_name)

        # Statusni yangilash
        task.status = new_status
        task.save()

        return redirect("user_status", id=task_id)  # Sahifani qayta yuklash

    return redirect("home")  # Noto‘g‘ri so‘rov bo‘lsa, bosh sahifaga yo‘naltiramiz
