from django.db import models



class Position(models.Model):

    name = models.CharField(max_length=50)

    
# Create your models here.
class Users(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)



