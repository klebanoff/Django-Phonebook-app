from django.urls import path
from . import views
# pylint: disable=no-member
app_name = 'phonebook'
urlpatterns = [
    path('',views.departments,name='departments'),
    path('0/',views.departments),
    path('<int:department_id>/',views.department,name='department'),
    path('<int:department_id>/new',views.newdepartment,name='newdepartment'),
    path('<int:department_id>/delete',views.deletedepartment,name='deletedepartment'),
    path('<int:department_id>/newemployee',views.newemployee,name='newemplyee'),
    path('employee/<int:employee_id>',views.employee,name='employee'),
    path('employee/<int:employee_id>/edit',views.editemployee,name='editemployee'),
    path('employee/<int:employee_id>/delete',views.delemployee,name='deleteemployee'),
    path('employee/all',views.allemployee,name='search'),
]
