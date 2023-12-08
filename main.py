from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Pydantic model for student data
class Student(BaseModel):
    id: int
    student_name: str
    score: float

app = FastAPI()

# Function to load data from the JSON file
def load_data():
    with open("students.json", "r") as file:
        return json.load(file)

# Function to save data to the JSON file
def save_data(students):
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

# POST endpoint to add a student
@app.post("/students/")
async def create_student(student: Student):
    students = load_data()
    students.append(student.dict())
    save_data(students)
    return {"message": "Student added successfully"}

# GET endpoint to get all students
@app.get("/students/")
async def get_all_students():
    return load_data()

# GET endpoint to get a student's score by ID
@app.get("/students/{student_id}")
async def get_student_score(student_id: int):
    students = load_data()
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
