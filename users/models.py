from django.forms import ValidationError
from django.utils.timezone import now
from django.db import models



class Position(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
# Create your models here.
class Users(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class UserStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Teg(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Tasks(models.Model):
    # Tasks modeli harbir userlar uchun vazifalar beriladi
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now, blank=True)
    end_time = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(auto_now=True)  # Oxirgi yangilanish vaqti
    status = models.ForeignKey(UserStatus,on_delete=models.CASCADE)
    teg = models.ForeignKey(Teg,on_delete=models.CASCADE)

    
    def clean(self):
        if self.end_time and self.start_time and self.end_time < self.start_time:
            raise ValidationError({"end_time": "Tugash vaqti boshlanish vaqtidan oldin bo‘lishi mumkin emas!"})
        
    def save(self, *args, **kwargs):
        """ save() chaqirilganda avtomatik ravishda clean() ni ishlatiladi  """
        self.clean()  # Avval validatsiya
        super().save(*args, **kwargs)  # Keyin saqlash

    def __str__(self):
        return f"{self.name}"