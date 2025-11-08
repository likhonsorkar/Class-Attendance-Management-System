from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ClassRoom, Student, Attendance
from .forms import ClassRoomForm, StudentForm
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True 
    def get_success_url(self):
        return reverse_lazy('attendance:select_class')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome Back! Please Login'
        return context
@method_decorator(login_required, name='dispatch')
class Add_class(View):
        def get(self, request, *args, **kwargs):
            form = ClassRoomForm()
            return render(request, 'attendance/add_class.html', {'form': form})
        def post(self, request, *args, **kwargs):
            form = ClassRoomForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('attendance:select_class')
@method_decorator(login_required, name='dispatch')
class Add_Student(View):
    template_name = 'attendance/add_student.html'
    def get(self, request, class_id):
        classroom = get_object_or_404(ClassRoom, pk=class_id)
        form = StudentForm()
        context = {
            'form': form, 
            'classroom': classroom
        }
        return render(request, self.template_name, context)
    def post(self, request, class_id):
        classroom = get_object_or_404(ClassRoom, pk=class_id)
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('attendance:mark_attendance', class_id=class_id)
        context = {
            'form': form, 
            'classroom': classroom
        }
        return render(request, self.template_name, context)
@method_decorator(login_required, name='dispatch')
class Select_class(ListView):
    model = ClassRoom
    template_name = 'attendance/select_class.html'
    context_object_name = 'classes'
@method_decorator(login_required, name='dispatch')
class Mark_attendance(View):
    def get(self, request, class_id):
        classroom = get_object_or_404(ClassRoom, pk=class_id)
        students = classroom.students.all()
        return render(request, 'attendance/mark.html', 
                      {'classroom': classroom, 'students': students})

    def post(self, request, class_id):
        classroom = get_object_or_404(ClassRoom, pk=class_id)
        students = classroom.students.all()
        att_date = request.POST.get('date') or str(date.today())
        for student in students:
            is_present = request.POST.get(f'present_{student.id}') == 'on'
            status = 'P' if is_present else 'A'
            Attendance.objects.update_or_create(
                student=student,
                date=att_date,
                defaults={'status': status, 'classroom': classroom}
            )
        return redirect('attendance:summary', class_id=class_id)
@method_decorator(login_required, name='dispatch')
class Summary(View):
    def get(self, request, class_id):
        classroom = get_object_or_404(ClassRoom, pk=class_id)
        students = classroom.students.all()
        report = []
        for s in students:
            total = s.attendances.count()
            present = s.attendances.filter(status='P').count()
            percent = (present / total * 100) if total > 0 else 0
            report.append({
                'student': s, 
                'total': total, 
                'present': present, 
                'percent': round(percent, 2)
            })
        return render(request, 'attendance/summary.html', 
                      {'classroom': classroom, 'report': report})
    
def logout_acc(request):
    logout(request)
    return redirect('login')