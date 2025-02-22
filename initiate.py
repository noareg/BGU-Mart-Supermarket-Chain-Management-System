from persistence import *

import sys
import os

def add_branche(splittedline : list[str]):
    id, location, number_of_employees = splittedline
    repo.branches.insert(Branche(int(id), location, int(number_of_employees)))
    
def add_supplier(splittedline : list[str]):
    id, name, contact_information = splittedline
    repo.suppliers.insert(Supplier(int(id), name, contact_information))

def add_product(splittedline : list[str]):
    id, description, price, quantity = splittedline
    repo.products.insert(Product(int(id), description, float(price), int(quantity)))

def add_employee(splittedline : list[str]):
    id, name, salary, branche = splittedline
    repo.employees.insert(Employee(int(id), name, float(salary), int(branche)))
    
    
adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    repo._close()
    inputfilename = args[1]
    if os.path.exists("bgumart.db"):
        os.remove("bgumart.db")

    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)