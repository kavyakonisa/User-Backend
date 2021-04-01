# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    registrationDate=models.DateField("RegistrationDate", auto_now_add=True)
    profile_pic=models.ImageField(default='default.png',blank=True)
    is_student= models.BooleanField(default=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email



class Student(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='Student_profile',primary_key= True)
    study_class = models.IntegerField()
    bio = models.TextField(blank=True)
    



class Teacher(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='Teacher_profile',primary_key= True)
    subject = models.CharField(max_length=100)
    experience = models.IntegerField()



