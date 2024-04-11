import json
from models.students_models import Student

def check_if_valid_school_data(data):
    if not isinstance(data, dict) or 'students' not in data:
        raise ValueError("Invalid db structure: must be a dictionary with a 'students' key")

    if not isinstance(data['students'], list):
        raise ValueError("Invalid db structure: 'students' must be a list.")

def get_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
        return data

def write_data(file_path, data):
    with open(file_path, "r+") as f:
        f.seek(0)        
        json.dump(data,f, indent=4)
        f.truncate()
        return True

def get_all_students(file_path) -> list:
    data = get_data(file_path)
    check_if_valid_school_data(data)
    return data["students"]

def update_students_list(file_path, new_students_list: list):
    data = {"students": new_students_list}
    return write_data(file_path, data)

def get_student_by_id(file_path, all_students_list, id) -> tuple[int, Student]:
    for index, student in enumerate(all_students_list):
        if student["id"] == id:
            student_object = Student(**student)
            return index, student_object
    raise FileNotFoundError(f'Student with id {id} not in db')

def add_student(file_path, new_student):
    with open(file_path, "r+") as f:
        f.seek(0)
        school_data = json.load(f)
        all_students = school_data["students"]

        # make sure that this student does not already exist:
        for student in all_students:
            if student["id"] == new_student.id:
                return {"Error": f"student with id {new_student.id} already exists"}
        
        # let's add the new student
        all_students.append(dict(new_student))
        f.seek(0)        
        json.dump(school_data,f, indent=4)
        f.truncate()
        
        return new_student

def delete_all_students(file_path) -> int | None:
    try:
        with open(file_path, "r+") as f:
            f.seek(0)
            content = f.read()
            content = json.loads(content)
            num_of_records = len(content["students"])
            content["students"].clear()
            f.seek(0)        
            json.dump(content,f, indent=4, sort_keys=True)
            f.truncate()

            return num_of_records
    except Exception as e:
        print(e)
        return None
    
def delete_student_by_id(file_path, id):
    all_students: list = get_all_students(file_path)
    for student in all_students:
        if student["id"] == id:
            all_students.remove(student)
            # update db
            update_students_list(file_path, all_students)
            return student
    raise FileNotFoundError(f'Student with id {id} not in db')

def log_to_file(data):
    print("Logging triggered!")
    print(data)