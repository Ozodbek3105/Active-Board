from django.contrib import admin

from users.models import Position, Tasks, Teg, UserStatus, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Position)

admin.site.register(UserStatus)
admin.site.register(Tasks)
admin.site.register(Teg)
