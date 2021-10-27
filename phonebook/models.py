from django.db import connection

# Create your models here.
def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class Department:
    """Содержит методы обращения к sqlite БД для таблицы departments. parentid - id департаметна родителя. Если parentid = 0 то это главный отдел без родителя"""
    def __init__(self):
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS departments(departmentid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,dname TEXT,parentid INT);")
    def getall(self):
    """Получение всех департаментов в виде списка словарей"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments")
            data = dictfetchall(cursor)
        return data
    def new(self, name, parentid):
    """Создание нового департамента"""
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO departments VALUES(NULL,%s,%s);",[name,parentid])
    def update(self, id, newname):
    """Обновление существующего департамента"""
        with connection.cursor() as cursor:
            cursor.execute("UPDATE departments SET dname = %s WHERE departmentid = %s",[newname,id])
    def delete(self, id):
    """Удаление департамента по id"""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM departments WHERE departmentid = %s", [id])
    def getbyparentid(self,parentid):
    """Получение всех департаментов по parentid в виде списка словарей"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments WHERE parentid = %s", [parentid])
            data = dictfetchall(cursor)
        return data
    def getbyid(self,id):
    """получение одного департамента в виде списка словарей"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM departments WHERE departmentid = %s", [id])
            data = dictfetchall(cursor)
        return data

class Employee:
    """Содержит методы обращения к sqlite БД для таблицы employees"""
    def __init__(self):
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS employees(employeeid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,surname TEXT, partonymic TEXT,email TEXT,phonenumber TEXT, departmentid INTEGER, FOREIGN KEY (departmentid) REFERENCES departments (departmentid) ON UPDATE CASCADE ON DELETE CASCADE);")
    def getall(self):
    """Получение всех сотрудника в виде списка словарей"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            data = dictfetchall(cursor)
        return data
    def new(self, name, surname, part, email, phonenumber, gepartmentid):
    """Создание нового сотрудника"""
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employees VALUES(NULL,%s,%s,%s,%s,%s,%s);",[name, surname, part, email, phonenumber, gepartmentid])
    def update(self, id, newname, newsurname, newpart, newemail, newphonenumber):
    """Обновление существующего сотрудника"""
        with connection.cursor() as cursor:
            cursor.execute("UPDATE employees SET name = %s, surname = %s, partonymic = %s, email = %s, phonenumber = %s WHERE employeeid = %s",[newname, newsurname, newpart, newemail, newphonenumber, id])
    def delete(self, id):
    """Удаление сотрудника по id"""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE employeeid = %s", [id])
    def getbyid(self,id):
    """Получене одного работника по id"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE employeeid = %s", [id])
            data = dictfetchall(cursor)
        return data
    def getbydepid(self,depid):
    """Получшение списка работников по departmentid"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees WHERE departmentid = %s", [depid])
            data = dictfetchall(cursor)
        return data