from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import Employee
from .forms import EmployeeForm


def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, "employee_detail.html", {"employee": employee})


@login_required
@permission_required('employees.add_employee', raise_exception=True)
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully 🎉")
            return redirect("home")
        else:
            messages.error(request, "Please fix the errors below ❌")
    else:
        form = EmployeeForm()

    return render(request, "add_employee.html", {"form": form})


@login_required
@permission_required('employees.add_employee', raise_exception=True)

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

    return render(request, "edit_employee.html", {"form": form, "employee": employee})


@login_required
@permission_required('employees.add_employee', raise_exception=True)

def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.is_active = False
        employee.save()
        messages.success(request, "Employee deleted successfully 🗑️")
        return redirect("home")

    return render(request, "employee_confirm_delete.html", {"employee": employee})


@login_required
@permission_required('employees.add_employee', raise_exception=True)

def employee_restore(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.is_active = True
    employee.save()
    messages.success(request, "Employee restored successfully ♻️")
    return redirect("home")
