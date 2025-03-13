from django.contrib import admin

from users.models import Position, Tasks, Teg, UserProfile, UserStatus

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Position)

admin.site.register(UserStatus)
admin.site.register(Tasks)
admin.site.register(Teg)
