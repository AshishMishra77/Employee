from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import Employee
from .forms import EmployeeForm
from accounts.forms import LoginForm, RegisterForm


# ================= HOME =================

# @login_required(login_url="login")
def home(request):
    employees = Employee.objects.all()
    return render(request, "home.html", {"employees": employees})


# ================= EMPLOYEE VIEWS =================

@login_required(login_url="login")
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, "employee_detail.html", {"employee": employee})


@login_required(login_url="login")
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully 🎉")
            return redirect("home")  # ✅ redirect only on success
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {"form": form})


@login_required(login_url="login")
def employee_edit(request, id):
    employee = get_object_or_404(Employee, id=id)

    if not employee.is_active:
        messages.error(request, "You cannot edit a deleted employee ❌")
        return redirect("home")

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully ✏️")
            return redirect("employee_edit", id=employee.id)
        else:
            messages.error(request, "Please correct the errors below ❌")
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "edit_employee.html", {
        "form": form,
        "employee": employee
    })


@login_required(login_url="login")
def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)

    if not employee.is_active:
        messages.warning(request, "Employee is already deleted ⚠️")
        return redirect("home")

    if request.method == "POST":
        employee.is_active = False
        employee.save()
        messages.success(request, "Employee deleted successfully 🗑️")
        return redirect("home")

    return render(request, "employee_confirm_delete.html", {
        "employee": employee
    })


@login_required(login_url="login")
def employee_restore(request, id):
    employee = get_object_or_404(Employee, id=id)

    if employee.is_active:
        messages.info(request, "Employee is already active ℹ️")
    else:
        employee.is_active = True
        employee.save()
        messages.success(request, "Employee restored successfully ♻️")

    return redirect("home")


# ================= AUTH VIEWS =================

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "Logged in successfully ✅")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials or captcha ❌")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully 🎉")
            return redirect("login")
        else:
            messages.error(request, "Please fix the errors & captcha ❌")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})



