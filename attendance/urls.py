from django.urls import path
from .views import Select_class, Mark_attendance, Summary, Add_class, Add_Student, CustomLoginView

app_name = 'attendance'

urlpatterns = [
    path('', Select_class.as_view(), name='select_class'),
    path('add_class/', Add_class.as_view(), name='add_class'),
    path('class/<int:class_id>/add_student/', Add_Student.as_view(), name='add_student'),
    path('class/<int:class_id>/mark/', Mark_attendance.as_view(), name='mark_attendance'),
    path('class/<int:class_id>/summary/', Summary.as_view(), name='summary'),
]