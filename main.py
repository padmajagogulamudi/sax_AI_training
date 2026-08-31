from fastapi import FastAPI,Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session 
from database import engine, Base,SessionLocal,get_db
import models
app = FastAPI()
Base.metadata.create_all(bind=engine)
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
class Student(BaseModel):
    id:int
    name:str
    course:str
    dept:Optional[str]=None

@app.get("/")
def home():
    return {"message": "Hello World"}

# @app.get("/about")
# def aboutPage():
#     return {"msg":"this is about page"}
#-----------------------------------------
@app.get("/students")
def getStudents(db:Session=Depends(get_db)):
    #db=SessionLocal()
    students=db.query(models.Student).all()
    #db.close()
    
    return {
        "students":students,
        "msg":"getting students data successfully!!!"
    }
@app.post("/students")
def saveStudents(student : Student,db:Session=Depends(get_db)):
    # db=SessionLocal()
    new_student=models.Student(id=student.id,name=student.name,course=student.course,dept=student.dept)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    #db.close()
    
    return {"msg":"saving student data",
            "student":new_student}
#-----------------Path param---------------------------------------
@app.get("/getStudentById/{stuid}")#path param
def get_stu_info_of(sid :int):
    print(type(sid))
    db=SessionLocal()
    stu=db.query(models.Student).filter(models.Student.id==sid).first()
    db.close()
    if stu is None:
        return{"msg":"stu not found with givven id"}
    return stu
    # for stu in students:
    #     if stu["id"] == sid:
    #         return stu
    # return {
    #     "msg":f"student with {sid} not found"
    # }
@app.get("/student/{stu_id}/course/{c_id}")#multi path
def get_details(cid:int,sid:int):
    return {
        "sid":cid,
        "cid":sid
    }

@app.get("/search")#Query param
def search_stu(name :str,db:Session=Depends(get_db)):
    stu= db.query(models.Student).filter(models.Student.name==name).first()
    if stu is None:
        return {"msg":"stu not found with givven name"}
    return {
        "student ": stu
    }

# @app.get("/stu")#optional query param
# def get_details(name:Optional[str]=None):
#     return {"name from optional param":name}
# @app.get("/stu")#multiple query param
# def get_details(name:str,age:int):
#     return {
#         "name":name,
#         "age":age
#     }
#-----------------post request---------------------------------------
# @app.post("/post_Stu")
# def posting_stu(student :Student):
#     return {
#         "stu":student,
#         "msg":"posting student"
#     }
#--------------------put request------------------------------------------
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student,db:Session=Depends(get_db)):
    #db=SessionLocal()
    old_stu=db.query(models.Student).filter(models.Student.id==student_id).first()
    if old_stu is None:
        return{"msg":"not found"}
    old_stu.name=student.name
    old_stu.course=student.course
    old_stu.dept=student.dept
    db.commit()
    db.refresh(old_stu)
    #db.close()
    

    # for s in students:

    #     if s["id"] == student_id:
    #         s["name"] = student.name
    #         s["course"] = student.course

    #         return {
    #             "message": "Student updated successfully",
    #             "student": s
    #         }

    return {
        "message": "Student updated",
        "stu":old_stu
    }
#------------------delete request------------------------------------
@app.delete("/remove_Stu/{sid}")
def removeStu(sid :int,db:Session=Depends(get_db)):
   # db=SessionLocal()
    old_stu=db.query(models.Student).filter(models.Student.id==sid).first()
    if old_stu  is None:
        return{
            "msg":"not found"
        }
    db.delete(old_stu)
    db.commit()
    #db.close()
    return{"msg":"deleted successfully"}
    # for s in students:
    #     if s["id"]==sid:
    #         students.remove(s)
    #         return{
    #             "msg":"removing student",
    #             "stu":s
    #         }
    # return{
    #     "msg":"student not found"
    # }