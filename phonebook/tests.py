from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

from phonebook.models import Department, Employee


class DepartmentsIndexView(TestCase):
    def test_nodepartments(self):
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не добавлено ни одного отдела")
        self.assertQuerysetEqual(response.context['departments_dictlist'], [])
    def test_onedepartment(self):
        db = Department()
        db.new('Отдел',0)
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")
    def test_deletedep(self):
        db = Department()
        db.new('Отдел',0)
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")
        id = 1
        db.delete(id)
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не добавлено ни одного отдела")
        self.assertQuerysetEqual(response.context['departments_dictlist'], [])
class DepartamentView(TestCase):
    def test_viewdep(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        response = self.client.get(reverse('phonebook:department', args=(id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")
    def test_rename(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        response = self.client.get(reverse('phonebook:department', args=(id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")
        client = Client()
        client.post(reverse('phonebook:department', args=(id,)),
                    {'department_name': 'Редактирование тест'})
        response = self.client.get(reverse('phonebook:department', args=(id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Редактирование тест")
class DeleteDepView(TestCase):
    def test_deletedep(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        response = self.client.get(reverse('phonebook:deletedepartment', args=(id,)))
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не добавлено ни одного отдела")
        self.assertQuerysetEqual(response.context['departments_dictlist'], [])
class NewDepView(TestCase):
    def test_createdep(self):
        client = Client()
        client.post(reverse('phonebook:newdepartment', args=(0,)),
                    {'department_name': 'Отдел'})
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")
class NewEmployeeView(TestCase):
    def test_newempl(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        client = Client()
        client.post(reverse('phonebook:newemplyee', args=(id,)),
                    {'name': 'Имя',
                     'surname': 'Фамилия',
                     'partonymic': 'Отчество',
                     'email': 'Email',
                     'phonenumber': 'номер телефона'})
        response = self.client.get(reverse('phonebook:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Имя")             
class DeleteEmployee(TestCase):
    def test_deleteempoyee(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        client = Client()
        client.post(reverse('phonebook:newemplyee', args=(id,)),
                    {'name': 'Имя',
                     'surname': 'Фамилия',
                     'partonymic': 'Отчество',
                     'email': 'Email',
                     'phonenumber': 'номер телефона'})
        response = self.client.get(reverse('phonebook:deleteemployee', args=(1,)))
        response = self.client.get(reverse('phonebook:search'))
        self.assertQuerysetEqual(response.context['employees'], [])
class EmployeeView(TestCase):
    def test_employeeview(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        client = Client()
        client.post(reverse('phonebook:newemplyee', args=(id,)),
                    {'name': 'Имя',
                     'surname': 'Фамилия',
                     'partonymic': 'Отчество',
                     'email': 'Email',
                     'phonenumber': 'номер телефона'})
        response = self.client.get(reverse('phonebook:employee', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Имя")          
class Search(TestCase):
    def test_search(self):
        db = Department()
        db.new('Отдел',0)
        id = 1
        client = Client()
        client.post(reverse('phonebook:newemplyee', args=(id,)),
                    {'name': 'Имя',
                     'surname': 'Фамилия',
                     'partonymic': 'Отчество',
                     'email': 'Email',
                     'phonenumber': 'номер телефона'})
        client.post(reverse('phonebook:newemplyee', args=(id,)),
                    {'name': '2Имя',
                     'surname': '2Фамилия',
                     'partonymic': '2Отчество',
                     'email': '2Email',
                     'phonenumber': '2номер телефона'})
        response = client.get('/phonebook/employee/all?q=Имя')
        employees = Employee()
        employee = employees.getbyid(1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Имя")              
        self.assertQuerysetEqual(response.context['employees'], employee)           
                   