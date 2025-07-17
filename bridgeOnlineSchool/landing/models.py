from django.db import models
from django.contrib.auth.models import User



class Teacher(models.Model):

    # possibility to connect the teacher field to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    experience = models.CharField(max_length=500)
    teaching_years = models.IntegerField(max_length=2, null=True, blank=True)
    champion = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='teachers/avatars')
    lesson_price = models.DecimalField(max_digits=6, decimal_places=0)
    course_price = models.DecimalField(max_digits=7, decimal_places=0)

    # is listing active 
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
