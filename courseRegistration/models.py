from django.db import models
from django.contrib.auth.models import User

#Table for User
class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)
    advisor = models.BooleanField(default = False)
    netId = models.CharField(max_length=25)
    netPassword = models.CharField(max_length=50)
    major = models.CharField(
        max_length=5,
        choices=(
            ("math", "MATH"),
            ("cs", "CS")
        ),
        default = "CS",
    )

    def __str__(self):
        return self.user.username
    
#Table for Courses Taken
class CourseTaken(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=20)

    def __str__(self):
        return self.course.title
    
class ScheduleAs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    scheduleAs = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduleas")