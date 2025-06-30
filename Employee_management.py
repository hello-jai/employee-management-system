import json
from abc import ABC, abstractmethod

# Abstract Base Employee Class
class Employee(ABC):
    def __init__(self, employee_id: str, name: str, department: str):
        self._employee_id = employee_id
        self._name = name
        self._department = department

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = value

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    def display_details(self) -> str:
        return f"ID: {self._employee_id}, Name: {self._name}, Dept: {self._department}"

    def to_dict(self) -> dict:
        return {
            'employee_id': self._employee_id,
            'name': self._name,
            'department': self._department
        }

# Full Time Employee Class
class FullTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float):
        super().__init__(employee_id, name, department)
        self._monthly_salary = monthly_salary

    @property
    def monthly_salary(self):
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value):
        if value >= 0:
            self._monthly_salary = value
        else:
            print("Monthly salary cannot be negative")

    def calculate_salary(self) -> float:
        return self._monthly_salary

    def display_details(self) -> str:
        base_details = super().display_details()
        return f"{base_details}, Monthly Salary: ₹{self._monthly_salary}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'monthly_salary': self._monthly_salary,
            'type': 'fulltime'
        })
        return data

# Part Time Employee Class
class PartTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, hourly_rate: float, hours_worked_per_month: float):
        super().__init__(employee_id, name, department)
        self._hourly_rate = hourly_rate
        self._hours_worked_per_month = hours_worked_per_month

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        if value >= 0:
            self._hourly_rate = value
        else:
            print("Hourly rate cannot be negative")

    @property
    def hours_worked_per_month(self):
        return self._hours_worked_per_month

    @hours_worked_per_month.setter
    def hours_worked_per_month(self, value):
        if value >= 0:
            self._hours_worked_per_month = value
        else:
            print("Hours worked cannot be negative")

    def calculate_salary(self) -> float:
        return self._hourly_rate * self._hours_worked_per_month

    def display_details(self) -> str:
        base_details = super().display_details()
        return f"{base_details}, Hourly Rate: ₹{self._hourly_rate}, Hours/Month: {self._hours_worked_per_month}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'hourly_rate': self._hourly_rate,
            'hours_worked_per_month': self._hours_worked_per_month,
            'type': 'parttime'
        })
        return data

# Manager Class (inherits from FullTimeEmployee)
class Manager(FullTimeEmployee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float, bonus: float):
        super().__init__(employee_id, name, department, monthly_salary)
        self._bonus = bonus

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, value):
        if value >= 0:
            self._bonus = value
        else:
            print("Bonus cannot be negative")

    def calculate_salary(self) -> float:
        return super().calculate_salary() + self._bonus

    def display_details(self) -> str:
        base_details = super().display_details()
        return f"{base_details}, Bonus: ₹{self._bonus}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'bonus': self._bonus,
            'type': 'manager'
        })
        return data

# Company Class
class Company:
    def __init__(self, data_file: str = 'employees.json'):
        self._employees = {}
        self._data_file = data_file
        self._load_data()

    def _load_data(self):
        try:
            with open(self._data_file, 'r') as file:
                data = json.load(file)
                for emp in data:
                    emp_type = emp.get('type')
                    if emp_type == 'fulltime':
                        employee = FullTimeEmployee(
                            emp['employee_id'], emp['name'], emp['department'], emp['monthly_salary'])
                    elif emp_type == 'parttime':
                        employee = PartTimeEmployee(
                            emp['employee_id'], emp['name'], emp['department'],
                            emp['hourly_rate'], emp['hours_worked_per_month'])
                    elif emp_type == 'manager':
                        employee = Manager(
                            emp['employee_id'], emp['name'], emp['department'],
                            emp['monthly_salary'], emp['bonus'])
                    else:
                        continue
                    self._employees[emp['employee_id']] = employee
        except FileNotFoundError:
            print("No existing employee data found. Starting with empty database.")
        except json.JSONDecodeError:
            print("Invalid JSON file format. Starting with empty database.")

    def _save_data(self):
        try:
            with open(self._data_file, 'w') as file:
                data = [employee.to_dict() for employee in self._employees.values()]
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_employee(self, employee: Employee) -> bool:
        if employee.employee_id in self._employees:
            return False
        self._employees[employee.employee_id] = employee
        self._save_data()
        return True

    def remove_employee(self, employee_id: str) -> bool:
        if employee_id in self._employees:
            del self._employees[employee_id]
            self._save_data()
            return True
        return False

    def find_employee(self, employee_id: str):
        return self._employees.get(employee_id, None)

    def search_employee_by_name(self, name: str):
        found_employees = []
        for employee in self._employees.values():
            if name.lower() in employee.name.lower():
                found_employees.append(employee)
        return found_employees

    def calculate_total_payroll(self) -> float:
        total = 0
        for employee in self._employees.values():
            total += employee.calculate_salary()
        return total

    def display_all_employees(self):
        if not self._employees:
            print("No employees found.")
            return

        print("\n" + "="*80)
        print("ALL EMPLOYEES")
        print("="*80)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'User Type':<15} {'Details'}")
        print("-"*80)
        for employee in self._employees.values():
            user_type = type(employee).__name__
            base_details = employee.display_details()
            print(f"{employee.employee_id:<10} {employee.name:<20} {employee.department:<15} {user_type:<15} {base_details}")
        print("="*80)

    def generate_payroll_report(self):
        if not self._employees:
            print("No employees found.")
            return

        print("\n" + "="*100)
        print("PAYROLL REPORT")
        print("="*100)
        print(f"{'ID':<10} {'Name':<20} {'Dept':<15} {'Type':<15} {'Salary':<15}")
        print("-"*100)

        total_payroll = 0
        for employee in self._employees.values():
            salary = employee.calculate_salary()
            total_payroll += salary
            user_type = type(employee).__name__
            print(f"{employee.employee_id:<10} {employee.name:<20} {employee.department:<15} {user_type:<15} ₹{salary:<14.2f}")

        print("-"*100)
        print(f"{'TOTAL PAYROLL:':<75} ₹{total_payroll:.2f}")
        print("="*100)

# Main Application Interface
def main():
    company = Company()

    while True:
        print("\n" + "="*50)
        print("EMPLOYEE MANAGEMENT SYSTEM v1.0\n \t\t\t By Jai , Aditya & Himanshu")
        print("="*50)
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Search Employee by ID")
        print("4. Search Employee by Name")
        print("5. Display All Employees")
        print("6. Calculate Total Payroll")
        print("7. Generate Payroll Report")
        print("8. Exit")
        print("="*50)

        try:
            choice = input("Enter your choice (1-8): ").strip()

            if choice == '1':
                while True:
                    print("\nEmployee Types:")
                    print("1. Full-time Employee")
                    print("2. Part-time Employee")
                    print("3. Manager")
                    print("0. Back to Main Menu")

                    emp_type = input("Select employee type (0-3): ").strip()
                    if emp_type == '0':
                        break

                    emp_id = input("Enter Employee ID: ").strip()
                    if company.find_employee(emp_id):
                        print("Employee with this ID already exists!")
                        continue

                    name = input("Enter Employee Name: ").strip()
                    department = input("Enter Department: ").strip()

                    if emp_type == '1':
                        try:
                            monthly_salary = float(input("Enter Monthly Salary: ₹"))
                            employee = FullTimeEmployee(emp_id, name, department, monthly_salary)
                        except ValueError:
                            print("Invalid salary amount!")
                            continue

                    elif emp_type == '2':
                        try:
                            hourly_rate = float(input("Enter Hourly Rate: ₹"))
                            hours_worked = float(input("Enter Hours Worked per Month: "))
                            employee = PartTimeEmployee(emp_id, name, department, hourly_rate, hours_worked)
                        except ValueError:
                            print("Invalid input!")
                            continue

                    elif emp_type == '3':
                        try:
                            monthly_salary = float(input("Enter Monthly Salary: ₹"))
                            bonus = float(input("Enter Monthly Bonus: ₹"))
                            employee = Manager(emp_id, name, department, monthly_salary, bonus)
                        except ValueError:
                            print("Invalid input!")
                            continue

                    else:
                        print("Invalid employee type!")
                        continue

                    if company.add_employee(employee):
                        print("Employee added successfully!")
                    else:
                        print("Failed to add employee!")
                    break

            elif choice == '2':
                emp_id = input("Enter Employee ID to remove (or 0 to cancel): ").strip()
                if emp_id == '0':
                    continue
                if company.remove_employee(emp_id):
                    print("Employee removed successfully!")
                else:
                    print("Employee not found!")

            elif choice == '3':
                emp_id = input("Enter Employee ID to search (or 0 to cancel): ").strip()
                if emp_id == '0':
                    continue
                employee = company.find_employee(emp_id)
                if employee:
                    print("\nEmployee Found:")
                    print("-" * 40)
                    print(employee.display_details())
                    print(f"Monthly Salary: ₹{employee.calculate_salary():.2f}")
                else:
                    print("Employee not found!")

            elif choice == '4':
                name = input("Enter Employee Name to search (or 0 to cancel): ").strip()
                if name == '0':
                    continue
                employees = company.search_employee_by_name(name)
                if employees:
                    print(f"\nFound {len(employees)} employee(s):")
                    print("-" * 40)
                    for emp in employees:
                        print(emp.display_details())
                else:
                    print("No employees found with that name!")

            elif choice == '5':
                company.display_all_employees()

            elif choice == '6':
                total = company.calculate_total_payroll()
                print(f"\nTotal Company Payroll: ₹{total:.2f}")

            elif choice == '7':
                company.generate_payroll_report()

            elif choice == '8':
                print("Thank you for using Employee Management System!")
                break

            else:
                print("Invalid choice! Please enter a number between 1-8.")

        except KeyboardInterrupt:
            print("\n\nExiting Employee Management System...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
