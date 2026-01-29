from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.employee_detail, name="employee_detail"),
    path("add/", views.add_employee, name="add_employee"),
    path("<int:id>/edit/", views.employee_edit, name="employee_edit"),
    path("<int:id>/delete/", views.employee_delete, name="employee_delete"),
    path("restore/<int:id>/", views.employee_restore, name="employee_restore"),
]
