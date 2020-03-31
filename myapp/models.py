from django.db import models
from django.contrib.auth.models import User

DOMAIN_CHOICES = (
   ('Engineering','Engineering'),
   ('Management','Management'),
   ('Both','Both')
)

FORUM_TYPE_CHOICES = (
    ('Announcement', 'Announcement'),
    ('CollegeLevel', 'CollegeLevel'),
    ('DepartmentLevel', 'DepartmentLevel'),
    ('SemesterLevel', 'SemesterLevel'),
)

DEPARTMENT_CHOICES = (
    ('Computer_Science', 'Computer_Science'),
    ('Information_Technology', 'Information_Technology'),
    ('Electronics_Engineering', 'Electronics_Engineering'),
    ('Electrical_Engineering', 'Electrical_Engineering'),
    ('Instrumentation_Engineering', 'Instrumentation_Engineering'),
    ('Mechanical_Engineering', 'Mechanical_Engineering'),
    ('Civil_Engineering', 'Civil_Engineering'),
    ('MBA', 'MBA'),
    ('Chemical', 'Chemical'),
)

# Create your models here.
class College(models.Model):
    college = models.AutoField(primary_key=True)
    applicant_id = models.CharField(max_length=200, null=False)
    college_name = models.CharField(max_length=50, null=False)
    university = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    contact_number = models.CharField(max_length=15, null=False)
    logo = models.ImageField(upload_to = 'logos/')
    domain = models.TextField(max_length=100, choices=DOMAIN_CHOICES)
    about_us = models.TextField(max_length=1000, null=False)
    image1 = models.ImageField(upload_to = 'slider/', null=False)
    image2 = models.ImageField(upload_to = 'slider/', null=True)
    image3 = models.ImageField(upload_to = 'slider/', null=True)
    image4 = models.ImageField(upload_to = 'slider/', null=True)
    image5 = models.ImageField(upload_to = 'slider/', null=True)

class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=False)
    department_id = models.AutoField(primary_key=True)
    department_name = models.TextField(max_length=100,choices=DEPARTMENT_CHOICES)
    hod = models.TextField(max_length=100)
    count = models.CharField(max_length=50)
    vision_mission = models.TextField(max_length=1000, null=False)

class Teacher(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=50, null=False)

class Student(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    roll_number = models.CharField(primary_key=True, max_length=200)
    semester = models.IntegerField(null=False)

class Subject(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=False)
    semester = models.IntegerField(null=False)
    taught_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.subject_id)

class Syllabus(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.IntegerField(null=False)
    unit_name = models.CharField(max_length=10, null=False)
    topics = models.TextField(max_length=1000, null=False)

    def __str__(self):
        return self.unit_name

class SyllabusStatus(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)

class SyllabusStatusTeacher(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False)

class Forum(models.Model):
    forum_id = models.AutoField(primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    semester = models.IntegerField(null=True)
    forum_type = models.TextField(max_length=100, choices=FORUM_TYPE_CHOICES)

class ForumMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, null=False)
    sent_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(null=True)
    isAnonymous = models.BooleanField(default=False)

class UpcomingEvents(models.Model):
    event_id = models.AutoField(primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null = False)
    event_name = models.CharField(max_length=50, null = False)
    event_description = models.TextField(max_length=500, null = False)
    event_image = models.ImageField(upload_to = 'events/', null = True)
    start_date = models.DateField(null = False)
    end_date = models.DateField(null = False)