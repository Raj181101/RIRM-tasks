from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    roll_no = models.CharField(max_length=100, blank=True, null=True,unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.roll_no


class StudentAcademics(models.Model):
    roll_no = models.ForeignKey(StudentInfo,on_delete=models.CASCADE,null=True,blank=True)
    maths = models.FloatField(blank=True, null=True)
    physics = models.FloatField(blank=True, null=True)
    chemistry = models.FloatField(blank=True, null=True)
    biology = models.FloatField(blank=True, null=True)
    english = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return self.roll_no.roll_no