from django.contrib import admin

# Register your models here.
from attendance.models import ClassRoom, Student, Attendance

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll', 'classroom')
    list_filter = ('classroom',)
    search_fields = ('name', 'roll')
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'date', 'status')
    list_filter = ('date', 'classroom', 'status')
    search_fields = ('student__name', 'student__roll')