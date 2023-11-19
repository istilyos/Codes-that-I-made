class Student:
    def __init__(self, name, address, id_number, department):
        self.name = name
        self.address = address
        self.id_number = id_number
        self.department = department


class StudentDatabase:
    def __init__(self):
        self.students = []

    def register_student(self, name, address, id_number, department):
        student = Student(name, address, id_number, department)
        self.students.append(student)

    def inquire_by_department(self, department):
        result = []
        for i, student in enumerate(self.students, 1):
            if student.department == department:
                result.append((i, student))
        return result

    def inquire_by_name(self, name):
        result = []
        for i, student in enumerate(self.students, 1):
            if student.name == name:
                result.append((i, student))
        return result

    def inquire_by_id(self, id_number):
        result = []
        for i, student in enumerate(self.students, 1):
            if student.id_number == id_number:
                result.append((i, student))
        return result

    def display_all_students(self):
        return self.students

    def edit_student_info(self, department):
        students_in_department = self.inquire_by_department(department)
        if students_in_department:
            print(f"Students in the {department} department:")
            for i, student in enumerate(students_in_department, 1):  # Use enumerate with start=1
                print(
                    f"{i} - Name: {student[1].name}, Address: {student[1].address}, ID Number: {student[1].id_number}")

            index = int(input("Enter the index of the student you want to edit: "))
            if 1 <= index <= len(students_in_department):
                student = students_in_department[index - 1][1]
                name = input("Enter new name: ")
                address = input("Enter new address: ")
                id_number = input("Enter new ID number: ")
                department = input("Enter new department (IT/CS/DevCom): ")
                student.name = name
                student.address = address
                student.id_number = id_number
                student.department = department
                print("Student information updated successfully!")
            else:
                print("Invalid index. Please try again.")
        else:
            print(f"No students found in the {department} department.")

    def delete_student_by_index(self, index):
        if 1 <= index <= len(self.students):
            deleted_student = self.students.pop(index - 1)
            print(f"Deleted Student - Name: {deleted_student.name}, Address: {deleted_student.address}, ID Number: {deleted_student.id_number}")
        else:
            print("Invalid index. Please try again.")

    def delete_students_by_department(self, department):
        students_in_department = self.inquire_by_department(department)
        if students_in_department:
            print(f"Students in the {department} department:")
            for i, student in students_in_department:
                print(f"{i} - Name: {student.name}, Address: {student.address}, ID Number: {student.id_number}")

            index = int(input("Enter the index of the student you want to delete: "))
            self.delete_student_by_index(index)
        else:
            print(f"No students found in the {department} department.")


# Main program
database = StudentDatabase()

while True:
    print("Choose an option:")
    print("1. Register")
    print("2. Inquire")
    print("3. Edit Student Info")
    print("4. Delete Students Info")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        while True:
            name = input("Enter name: ")
            if name.strip() == "":
                print("Name cannot be blank. Please try again.")
                continue
            address = input("Enter address: ")
            if address.strip() == "":
                print("Address cannot be blank. Please try again.")
                continue
            id_number = input("Enter ID number: ")
            if id_number.strip() == "":
                print("ID number cannot be blank. Please try again.")
                continue

            department = input("Enter department (IT/CS/DevCom): ")
            if department in ["IT", "CS", "DevCom"]:
                break
            else:
                print("Invalid department. Please choose from IT, CS, or DevCom.")
        database.register_student(name, address, id_number, department)
        print("Student registered successfully!")

    elif choice == "2":
        while True:
            print("Choose an inquiry option:")
            print("a. Inquire by Department")
            print("b. Inquire by Name")
            print("c. Inquire by ID Number")
            print("d. Display All Students")
            print("e. Back")

            inquiry_choice = input("Enter your inquiry choice (a/b/c/d/e): ").lower()

            if inquiry_choice == "a":
                while True:
                    department = input("Enter department to inquire about (IT/CS/DevCom): ")
                    if department in ["IT", "CS", "DevCom"]:
                        break
                    else:
                        print("Invalid department. Please choose from IT, CS, or DevCom.")
                students = database.inquire_by_department(department)
                if students:
                    print(f"Students in the {department} department:")
                    for i, student in students:
                        print(f"{i} - Name: {student.name}, Address: {student.address}, ID Number: {student.id_number}")
                else:
                    print(f"No students found in the {department} department.")

            elif inquiry_choice == "b":
                name = input("Enter name to inquire about: ")
                students = database.inquire_by_name(name)
                if students:
                    print(f"Students with the name {name}:")
                    for i, student in students:
                        print(f"{i} - Department: {student.department}, Address: {student.address}, ID Number: {student.id_number}")
                else:
                    print(f"No students found with the name {name}.")

            elif inquiry_choice == "c":
                id_num = input("Enter ID number to inquire about: ")
                students = database.inquire_by_id(id_num)
                if students:
                    print(f"Students with ID number {id_num}:")
                    for i, student in students:
                        print(f"{i} - Name: {student.name}, Department: {student.department}, Address: {student.address}, ID Number: {student.id_number}")
                else:
                    print(f"No students found with the ID Number of {id_num}.")

            elif inquiry_choice == "d":
                all_students = database.display_all_students()
                if all_students:
                    print("All Registered Students:")
                    for i, student in enumerate(all_students, 1):
                        print(f"{i} - Name: {student.name}, Department: {student.department}, Address: {student.address}, ID Number: {student.id_number}")
                else:
                    print("No students registered yet.")

            elif inquiry_choice == "e":
                break

            else:
                print("Invalid inquiry choice. Please try again.")

    elif choice == "3":
        while True:
            print("Choose an edit option:")
            print("a. Edit by Department")
            print("b. Back")

            edit_choice = input("Enter your edit choice (a/b): ").lower()

            if edit_choice == "a":
                department = input("Enter the department of students you want to edit (IT/CS/DevCom): ")
                if department in ["IT", "CS", "DevCom"]:
                    database.edit_student_info(department)
                    break
                else:
                    print("Invalid department. Please choose from IT, CS, or DevCom.")
            elif edit_choice == "b":
                break
            else:
                print("Invalid edit choice. Please try again.")

    elif choice == "4":
        while True:
            print("Choose a delete option:")
            print("a. Delete by Department")
            print("b. Back")

            delete_choice = input("Enter your delete choice (a/b): ").lower()

            if delete_choice == "a":
                department = input("Enter the department of students you want to delete (IT/CS/DevCom): ")
                if department in ["IT", "CS", "DevCom"]:
                    database.delete_students_by_department(department)
                    break
                else:
                    print("Invalid department. Please choose from IT, CS, or DevCom.")
            elif delete_choice == "b":
                break
            else:
                print("Invalid delete choice. Please try again.")

    elif choice == "5":
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")



