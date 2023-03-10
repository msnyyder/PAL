from django.db import models
from django.contrib.auth.models import User

#Table for Schedule
class Schedule(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='schedule')
    name = models.CharField(max_length=50)
    semester = models.CharField(max_length = 6)
    year = models.IntegerField(default=2023)
    #courses could be saved as an array of the crn numbers
    #array fields will only work with Postgres database, finding another fix
    #courses = ArrayField(ArrayField(models.CharField(max_length=20)))
    courses = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Table for Course
class Course(models.Model):
    title = models.CharField(max_length=20)
    crn = models.CharField(max_length=20)
    creditHours = models.IntegerField(default = 0)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
#Table for Real Schedule
class RealSchedule(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='real_schedule')
    #grades = ArrayField(ArrayField(models.DecimalField(max_digits=5, decimal_places=2, default=0)))
    grades = models.CharField(max_length=20)

    def __str__(self):
        return self.schedule.name
    
#Table for Draft Schedules
class DraftSchedule(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='draft_schedule')
    advisorNotes = models.CharField(max_length=100)
    draftRanking = models.IntegerField(default = 1)

    def __str__(self):
        return self.schedule.name
