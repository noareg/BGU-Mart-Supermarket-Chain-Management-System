import sqlite3
import atexit
from dbtools import Dao, orm
 
# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, branche):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche = branche
 
class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

class Branche(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

class Activitie(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date
        
class EmployeeReportRow:
    def __init__(self, name, salary, location, total_sales):
        self.name = name
        self.salary = salary
        self.location = location
        self.total_sales = total_sales

class ActivityReportRow:
    def __init__(self, date, description, quantity, seller_name, supplier_name):
        self.date = date
        self.description = description
        self.quantity = quantity
        self.seller_name = seller_name
        self.supplier_name = supplier_name
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        #TODO: complete
        
        self.employees = Dao(Employee, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.products = Dao(Product, self._conn)
        self.branches = Dao(Branche, self._conn)   
        self.activities = Dao(Activitie, self._conn)
        
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    
    def get_employees_report(self):
        c = self._conn.cursor()
        c.execute("""
            SELECT e.name AS name,
                   e.salary AS salary,
                   b.location AS location,
                   IFNULL(SUM(
                     CASE WHEN a.quantity < 0 THEN p.price * -a.quantity
                          ELSE 0
                     END
                   ), 0) AS total_sales
            FROM employees e
            JOIN branches b ON e.branche = b.id
            LEFT JOIN activities a ON a.activator_id = e.id
            LEFT JOIN products p   ON a.product_id = p.id
            GROUP BY e.id
            ORDER BY e.name
        """)
        return orm(c, EmployeeReportRow)

    def get_activities_report(self):
        count_cursor = self._conn.cursor()
        count_cursor.execute("SELECT COUNT(*) FROM activities")
        total = count_cursor.fetchone()[0]
        if total == 0:
            return [] 
        c = self._conn.cursor()
        c.execute("""
            SELECT a.date            AS date,
                   p.description     AS description,
                   a.quantity        AS quantity,
                   CASE WHEN a.quantity < 0 THEN e.name ELSE 'None' END AS seller_name,
                   CASE WHEN a.quantity > 0 THEN s.name ELSE 'None' END AS supplier_name
            FROM activities a
            JOIN products p ON a.product_id = p.id
            LEFT JOIN employees e ON e.id = a.activator_id
            LEFT JOIN suppliers s ON s.id = a.activator_id
            ORDER BY a.date
        """)
        return orm(c, ActivityReportRow)
 
# singleton
repo = Repository()
atexit.register(repo._close)