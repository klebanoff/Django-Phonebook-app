from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

from phonebook.models import Department, Employee


class DepartmentsIndexView(TestCase):
    def test_nodepartments(self):
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не добавлено ни одного отдела")
        self.assertQuerysetEqual(response.context['departments_list'], [])
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
        id = db.getall[0].get('departmentid')
        db.delete(id)
        response = self.client.get(reverse('phonebook:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не добавлено ни одного отдела")
        self.assertQuerysetEqual(response.context['departments_list'], [])
class DepartamentView(TestCase):
    def test_viewdep(self):
        db = Department()
        db.new('Отдел',0)
        id = db.getall[0].get('departmentid')
        response = self.client.get(reverse('phonebook:department', args=(id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отдел")