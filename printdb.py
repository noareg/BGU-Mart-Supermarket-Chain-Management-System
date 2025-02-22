from persistence import *

def print_tables():
    print("Activities")
    activities = repo.activities.find_all_ordered_by_date()
    for activity in activities:
        print((activity.product_id, activity.quantity, activity.activator_id, activity.date))
    
    print("Branches")
    branches = repo.branches.find_all_ordered_by_id()
    for branche in branches:
        print((branche.id, branche.location, branche.number_of_employees))

    print("Employees")
    employees = repo.employees.find_all_ordered_by_id()
    for employee in employees:
        print((employee.id, employee.name, employee.salary, employee.branche))

    print("Products")
    products =repo.products.find_all_ordered_by_id()
    for product in products:
        print((product.id, product.description, product.price, product.quantity))

    print("Suppliers")
    suppliers = repo.suppliers.find_all_ordered_by_id()
    for supplier in suppliers:
        print((supplier.id, supplier.name, supplier.contact_information))
 
def print_employees_report():
    print("\nEmployees report")
    employees_report = repo.get_employees_report()
    for row in employees_report:
        print(row.name, row.salary, row.location, row.total_sales)

def print_activities_report():
    activities_report = repo.get_activities_report()
    if not activities_report:
        return  
    print("\nActivities report")
    for row in activities_report:
        print((row.date, row.description, row.quantity, row.seller_name, row.supplier_name))

def main():
    print_tables()
    print_employees_report()
    print_activities_report()

if __name__ == '__main__':
    main()