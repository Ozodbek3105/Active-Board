from django.contrib import admin

from users.models import Position, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Position)