from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

# Create your views here.

from .models import Department, Employee

def deletesub(db,dep_id):
    """Удаление отдела со всеми под-отделами"""
    department = db.getbyid(dep_id)
    subdepartments = db.getbyparentid(dep_id)
    for sub in subdepartments:
        id = sub.get('departmentid')
        if id != None:
            deletesub(db,id)
    db.delete(dep_id)

def departments(request):
    """Вид главной страницы с отделами"""
    db = Department()
    id = 0
    departments_dictlist = db.getbyparentid(id)
    return render(request, "phonebook/departments.html",
                      {'departments_dictlist': departments_dictlist,'parentid':id})

def department(request,department_id):
    """Вид с иофрмацией об отделе и редактированием отдела"""
    db = Department()
    employee = Employee()
    employees = employee.getbydepid(department_id)
    department = db.getbyid(department_id)
    departmentchild = db.getbyparentid(department_id)
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        db.update(department_id,department_name)
        return HttpResponseRedirect(reverse('phonebook:department', kwargs={'department_id': department_id}))
    return render(request, "phonebook/department.html",
                      {'department': department[0],'child':departmentchild,'employees':employees})
                      
def newdepartment(request,department_id):
    """Вид создания нового отдела"""
    db = Department()
    if request.method == "POST":
        department = request.POST.get("department_name")
        db.new(department,department_id)
        return HttpResponseRedirect(reverse('phonebook:departments'))
    return render(request, "phonebook/newdepartment.html")   
    
def deletedepartment(request,department_id):
    """Вид удаление отдела"""
    db = Department()
    deletesub(db,department_id)
    return HttpResponseRedirect(reverse('phonebook:departments'))

def newemployee(request,department_id):
    """Вид создания нового сотрудника"""
    db = Department()
    department_name = db.getbyid(department_id)[0].get('dname')
    if request.method == "POST":
        employee = Employee()
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        partonymic = request.POST.get("partonymic")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")
        employee.new(name,surname,partonymic,email,phonenumber,department_id)
        return HttpResponseRedirect(reverse('phonebook:department', kwargs={'department_id': department_id}))
    return render(request, "phonebook/new_employee.html",{'department_name':department_name})   

def employee(request,employee_id):
    """Вид информации об сотруднике"""
    db = Department()
    employee = Employee()
    employee_data = employee.getbyid(employee_id)
    department_name = db.getbyid(employee_data[0].get('departmentid'))[0].get('dname')
    return render(request, "phonebook/employee.html",{'employee':employee_data[0],'department_name':department_name}) 
    
def delemployee(request,employee_id):
    """Вид удаления сотрудника"""
    employee = Employee()
    department_id = employee.getbyid(employee_id)[0].get('departmentid')
    employee.delete(employee_id)
    return HttpResponseRedirect(reverse('phonebook:department', kwargs={'department_id': department_id}))
    
def editemployee(request,employee_id):
    """Вид редактирования сотрудника"""
    db = Department()
    employee = Employee()
    employee_data = employee.getbyid(employee_id)
    department_name = db.getbyid(employee_data[0].get('departmentid'))[0].get('dname')
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        partonymic = request.POST.get("partonymic")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")
        employee.update(employee_id,name,surname,partonymic,email,phonenumber)
        return HttpResponseRedirect(reverse('phonebook:employee', kwargs={'employee_id': employee_id}))
    return render(request, "phonebook/edit_employee.html",{'employee':employee_data[0],'department_name':department_name}) 
    
def allemployee(request):
    """Вид со всеми сотрудниками и поиск сотродников по ФИО"""
    employee = Employee()
    employees = employee.getall()
    if request.method == "GET":
        text = request.GET.get('q')
        if text is not None:
            words = text.split(' ')
            for word in words:
                searchresults = []
                for emp in employees:                   
                    if word == emp.get('name') or word == emp.get('surname') or word == emp.get('partonymic'):
                        searchresults.append(emp)
                employees = searchresults    
        return render(request, "phonebook/employees.html",{'employees':employees}) 
    return render(request, "phonebook/employees.html",{'employees':employees}) 
    