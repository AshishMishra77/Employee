from django.shortcuts import render
from employees.models import Employee
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request):
    employees = Employee.objects.all()
    return render(request, "home.html", {"employees": employees})
