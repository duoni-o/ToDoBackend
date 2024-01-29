from django.db import models

# Create your models here.
class Todo (models.Model) :
  id = models.AutoField(primary_key= True)
  userId = models.CharField(max_length = 50)
  title = models.CharField(max_length = 100)
  done = models.BooleanField(default = False)
  regDate = models.DateTimeField(auto_now_add = True)
  modDate = models.DateTimeField(null = True)