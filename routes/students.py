from fastapi import APIRouter, Path, HTTPException, Depends, Request
from typing import Optional, Annotated
from models.students_modal import Student
import utils.db_helper as db
import utils.auth_helper as auth
from utils.decorators import handle_errors, log_it

router = APIRouter()
DB_FILEPATH = "./data/school_database.json"

@handle_errors
@router.get("/students")
@log_it
def get_students(request: Request, is_admin: Annotated[bool, Depends(auth.verify_admin)], inclass: Optional[str] = None):
    """Root directory

    Returns:
        json: a list of all students
    """
    all_students = db.get_all_students(DB_FILEPATH)
    if not inclass:
        return all_students
    
    # If user is trying to filter by class, then make sure they are admin
    if not is_admin:
        raise HTTPException(status_code=401, detail="You don't have permission, only admins can filter by student class")
    
    students_in_class = [student for student in all_students if inclass.lower() in student["classes"]]
    return students_in_class

@log_it
@handle_errors
@router.get("/students/{id}")
def get_student_by_id(is_user: Annotated[bool, Depends(auth.verify_user)],id: int = Path(title="The ID of the student you want to get",
                                     description="It must be a non zero integer",
                                     gt=0)) -> Student:
    """Get a specific student by their unique id

    Args:
        id (int): must be a non zero positive integer

    Returns:
        student: of type Student
    """
    if not is_user:
        raise HTTPException(status_code=401, detail="Invalid user!")
    return db.get_student_by_id(DB_FILEPATH, id)

@log_it
@handle_errors
@router.post("/students")
def post_student(is_admin: Annotated[bool, Depends(auth.verify_admin)], new_student: Student) -> dict[str, str] | Student:
    """Add new students to the database

    Raises:
        HTTPException: User must be admin to use this enpoint, otherwise it returns a 401 code

    Returns:
        student: the new student object of type Student
    """
    if not is_admin:
        raise HTTPException(status_code=401, detail="You don't have permission, only admins can add students")
    
    add_result = db.add_student(DB_FILEPATH, new_student)
    return add_result

@log_it
@handle_errors
@router.delete("/students")
def delete_students(is_admin: Annotated[bool, Depends(auth.verify_admin)]) -> dict[str, str]:
    """Delete all students in the db (Admins only)
    """

    # If user is trying to filter by class, then make sure they are admin
    if not is_admin:
        raise HTTPException(status_code=401, detail="You don't have permission")
    
    print("Deleting!!")
    total_deleted_count = db.delete_all_students(DB_FILEPATH)

    # I can't simple use "if total_deleted_count:"  because in my case delete_all_students can return 0 which is a valid value.
    if total_deleted_count is not None:
        return {"message": f"{total_deleted_count} records have been deleted successfully!"}
    
    raise HTTPException(status_code=500, detail="Internal server error, deleting request failed.")

@log_it
@handle_errors
@router.delete("/students/{id}")
def delete_student_by_id(is_user: Annotated[bool, Depends(auth.verify_user)],id: int = Path(title="The ID of the student you want to delete",
                                     description="It must be a non zero integer",
                                     gt=0)) -> dict[str, str]:
    """Delete a specific student by their unique id

    Args:
        id (int): must be a non zero positive integer

    Returns:
        student: of type Student
    """

    try:
        if not is_user:
            raise HTTPException(status_code=401, detail="Invalid, you are not a registered user")
        deleted_student = db.delete_student_by_id(DB_FILEPATH, id)
        return {"message":f"student:{deleted_student['name']} with id {deleted_student['id']} was deleted successfully"}
    except FileNotFoundError as user_not_found:
        raise HTTPException(status_code=404, detail=f"Error: {user_not_found}")
