from fastapi import FastAPI

app = FastAPI()
students = [
    {
        "id": 1,
        "name": "Padmaja",
        "course": "Python"
    },
    {
        "id": 2,
        "name": "Rahul",
        "course": "Java"
    },
    {
        "id": 3,
        "name": "Priya",
        "course": "React"
    }
]

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def aboutPage():
    return {"msg":"this is about page"}
#-----------------------------------------
@app.get("/students")
def getStudents():
    return {
        "students":["rahul","priya","harini"],
        "msg":"getting students data successfully!!!"
    }
@app.post("/students")
def saveStudents():
    return {"msg":"saving student data"}
#--------------------------------------------------------
@app.get("/student/{stuid}")
def get_stu_info_of(sid : int):
    for stu in students:
        if stu["id"] == sid:
            return stu
    return {
        "msg":f"student with {sid} not found"
    }