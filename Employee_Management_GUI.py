import tkinter as tk
from tkinter import ttk
from datetime import date
from typing import List

#Employee class
class Employee:
    def __init__(self, id: str, name:str, birthday: date, salary_rate: float):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.salary_rate = salary_rate
        
    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Birthday: {self.birthday}, Salary Rate: {self.salary_rate}"

#Department class
class Department:
    def __init__(self, name: str):
        self.name = name
        self.employees: List[Employee] = []
        
    def add_employee(self, employee: Employee):
        self.employees.append(employee)
        
    def remove_employee(self, id : str):
        self.employees = [emp for emp in self.employees if emp.id != id]
        
    def __repr__(self):
        return f"Department name: {self.name}, employees = {len(self.employees)}"        
    
#Build GUI
#Step 1: Create a main window frame
root = tk.Tk()
root.title("Employee Management System")
root.geometry("800x550")

window_width = 800
window_height = 550

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Step 2: Generate components for the frame
#Top frame for department and search fields
top_frame = tk.Frame(root, background="#C6C6C6", padx = 12, pady = 12)
top_frame.pack(fill=tk.X)

#Department label and entry
department_label = tk.Label(top_frame, text="Department", background="#C6C6C6")
department_label.grid(row=0, column=0, padx= (0, 6), pady = 6)
department_entry = tk.Entry(top_frame)
department_entry.grid(row=0, column=1, padx = (0, 16), pady = 6)

#Search label and entry
search_label = tk.Label(top_frame, text="Search", background="#C6C6C6")
search_label.grid(row=0, column=2, padx = (0, 6), pady = 6)
search_entry = tk.Entry(top_frame)
search_entry.grid(row=0, column=3, padx = (0, 6), pady = 6)

#Middle frame for form field
form_frame = tk.Frame(root, background="#C6C6C6", padx = 12, pady = 12)
form_frame.pack(fill=tk.X)

fields = ["ID", "Name", "Birthday", "Salary rate"]
entries = {}

for i, field in enumerate(fields):
    label = tk.Label(form_frame, text=field + ":", background="#C6C6C6")
    label.grid(row=i, column=0, sticky="e", padx=(0, 12), pady=6)
    entry = tk.Entry(form_frame, width = 30)
    entry.grid(row=i, column=1, sticky="ew", pady=6)
    entries[field] = entry
    
form_frame.grid_columnconfigure(1, weight = 1)

#Bottom frame for buttons    
button_frame = tk.Frame(root, padx = 12, pady = 12)
button_frame.pack(fill=tk.X)

#Create add, edit, remove buttons
add_button = tk.Button(button_frame, text = "Add", width = 12)
edit_button = tk.Button(button_frame, text = "Edit", width = 12)
remove_button = tk.Button(button_frame, text = "Remove", width = 12)
add_button.pack(side = tk.LEFT, padx = (0, 6))
edit_button.pack(side = tk.LEFT, padx = (0, 6), expand = True)  
remove_button.pack(side = tk.RIGHT, padx = (0, 6))

#Frame for data table
table_frame = tk.Frame(root, padx = 12, pady = 12)
table_frame.pack(fill=tk.BOTH, expand = True)

# Table for displaying employees
columns = ("ordinal", "id", "name", "birthday", "salary")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

# Define headings
tree.heading("ordinal", text="Ordinals", anchor = tk.W)
tree.heading("id", text="ID", anchor = tk.W)
tree.heading("name", text="Name", anchor = tk.W)
tree.heading("birthday", text="Birthday", anchor = tk.W)
tree.heading("salary", text="Salary rate", anchor = tk.W)

# Define column widths
tree.column("ordinal", width=70, anchor = tk.W)
tree.column("id", width=100, anchor = tk.W)
tree.column("name", width=150, anchor = tk.W)
tree.column("birthday", width=100, anchor = tk.W)
tree.column("salary", width=100, anchor = tk.W)

# Add table to the frame
tree.pack(fill=tk.BOTH, expand=True)

#Step 4: Set event handlers
#Initialize an empty department
current_department = Department("Default Department")

#Refresh the table to display employees
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for i, emp in enumerate(current_department.employees, start = 1):
        tree.insert("", "end", values=(i, emp.id, emp.name, emp.birthday, emp.salary_rate))

#Add employee
def add_employee():
    id_ = entries["ID"].get()
    name = entries["Name"].get()
    birthday = entries["Birthday"].get()
    salary_rate = entries["Salary rate"].get()
    
    if not (id_ and name and birthday and salary_rate):
        print("All fields are required.")
        return
    
    try:
        birthday_date = date.fromisoformat(birthday)
        salary_rate_float = float(salary_rate)
        employee = Employee(id=id_, name=name, birthday=birthday_date, salary_rate=salary_rate_float)
        current_department.add_employee(employee)
        refresh_table()
    except ValueError as e:
        print(f"Invalid input: {e}")
        
#Edit selected employee
def edit_employee():
    selected_item = tree.selection()
    if not selected_item:
        print("No employee selected.")
        return
    
    item = tree.item(selected_item[0])
    values = item["values"]
    id_ = values[1]
    
    for emp in current_department.employees:
        if emp.id == id_:
            emp.name = entries["Name"].get() or emp.name
            try:
                emp.birthday = date.fromisoformat(entries["Birthday"].get()) or emp.birthday
                emp.salary_rate = float(entries["Salary rate"].get()) or emp.salary_rate
            except ValueError as e:
                print(f"Invalid input: {e}")
            break
    refresh_table()

# Remove selected employee
def remove_employee():
    selected_item = tree.selection()
    if not selected_item:
        print("No employee selected.")
        return
    
    item = tree.item(selected_item[0])
    id_ = item["values"][1]
    current_department.remove_employee(id_)
    refresh_table()

# Search employees
def search_employee(event):
    query = search_entry.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    
    filtered_employees = [
        (i, emp.id, emp.name, emp.birthday, emp.salary_rate)
        for i, emp in enumerate(current_department.employees, start=1)
        if query in emp.id.lower() or query in emp.name.lower()
    ]
    
    for emp in filtered_employees:
        tree.insert("", "end", values=emp)

# Bind button events
add_button.config(command=add_employee)
edit_button.config(command=edit_employee)
remove_button.config(command=remove_employee)
search_entry.bind("<KeyRelease>", search_employee)    

#Step 5: Start the Tkinter event loop
root.mainloop()
       
        
    