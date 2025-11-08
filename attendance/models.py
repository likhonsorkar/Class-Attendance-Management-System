from django.db import models

# Create your models here.
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.name} ({self.code})"
class Student(models.Model):
    name = models.CharField(max_length=200)
    roll = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    def __str__(self):
        return f"{self.name} - {self.roll}"

    class Meta:
        unique_together = ('roll', 'classroom')
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"