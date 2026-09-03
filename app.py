from flask import Flask,request
from database import get_db_connection

app = Flask(__name__)
# students = [
#     {
#         "id": 1,
#         "name": "kanna",
#         "course": "java"
#     },
#     {
#         "id": 2,
#         "name": "arun",
#         "course": "python"
#     },
#     {
#         "id": 3,
#         "name": "dolly",
#         "course": "java"
#     },
#     {
#         "id": 4,
#         "name": "rahul",
#         "course": "python"
#     },
#     {
#         "id": 5,
#         "name": "priya",
#         "course": "java"
#     },
#     {
#         "id": 6,
#         "name": "sneha",
#         "course": "javascript"
#     },
#     {
#         "id": 7,
#         "name": "vijay",
#         "course": "python"
#     },
#     {
#         "id": 8,
#         "name": "anusha",
#         "course": "java"
#     },
#     {
#         "id": 9,
#         "name": "rohit",
#         "course": "javascript"
#     },
#     {
#         "id": 10,
#         "name": "meena",
#         "course": "python"
#     }
# ]

@app.route("/")
def home():
    return "Welcome to Student Management System"
@app.route("/getStudentsList",methods=["GET"])#-----------get all-----------------------------------
def get_students():
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from students")
    stus=cursor.fetchall()
    cursor.close()
    connection.close()
    return {
        "msg": "getting students data",
        "students list ":stus
    }


@app.route("/get_stu/<int:sid>",methods=["GET"])#---------------------get by id=---------------------------
def get_by_id(sid):
    # for s in students:
    #     if s["id"]==sid:
    #         return s
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from students where id=%s",(sid,))
    stu=cursor.fetchone()
    if stu is None:
        cursor.close()
        connection.close()
        return "not found student with id"
    

    return{"stu":stu},200



@app.route("/students",methods=["POST"])#--------post request------------------------
def save_Student():
    data=request.get_json()

    connection=get_db_connection()
    cursor=connection.cursor()
    query="""INSERT INTO students (id, name, course) VALUES(%s,%s,%s)"""
    values=[data["id"],data["name"],data["course"]]
    cursor.execute(query,values)
    connection.commit()
    cursor.close()
    connection.close()
    # students.append(data)
    return {"msg":"Student saved",
            "Student":data}


@app.route("/get_by_course",methods=["GET"])#---------------get by course name--------------------------
def get_by_course_name():
    res=[]
    course=request.args.get("course").lower()
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from students where course=%s",(course,))
    res=cursor.fetchall()
    if len(res)==0:
        cursor.close()
        connection.close()
        return "no students on this course"
    cursor.close()
    connection.close()
    return {"stus":res}



    
    for s in students:
        if (s["course"]).lower() == course.lower():
            res.append(s)
    if len(res)>0:
        return res
    return "no students on that course"



# -------------------put request--------------------------------------------
@app.route("/update_stu/<int:sid>",methods=["PUT"])
def update_stu_by_Id(sid):
   
    data=request.get_json()
    # for s in students:
    #     if s["id"]==sid:
    #         if data["name"] not in ["string"]:
    #             s["name"]=data["name"]
    #         if data["course"] not in ["string"]:
    #             s["course"]=data["course"]
    #         return s
    # return "stu not found with given id"
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("select * from students where id=%s",(sid,))
    res=cursor.fetchone()
    if res == None:
        return "no studen with that id"
    
    name=res["name"]
    course=res["course"]
    query=""" update students set name=%s,course=%s where id=%s"""
    if data["name"] not in ["string"]:
        name=data["name"]
        
    if data["course"] not in ["string"]:
        course=data["course"]
    values=(name,course,sid)
    cursor.execute(query,values)
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return "not found student with id"
    cursor.close()
    connection.close()
    return "student with id updated"
    

#--------------------------delete by id-----------------------------
@app.route("/deleteStu/<int:sid>",methods=["DELETE"])
def remove_student(sid):
    connection=get_db_connection()
    cursor=connection.cursor(dictionary=True)    
    cursor.execute("select * from students where id=%s",(sid,))
    stu=cursor.fetchone()
    if stu is None:
            cursor.close()
            connection.close()
            return "stu not found"
    cursor.execute("delete from students where id=%s",(sid,))
    connection.commit()
    cursor.close()
    connection.close()
    # for s in students:()
    #     if s["id"]==sid:
    #         students.remove(s)
    #         return s
    # return "not found",401
    return "deleted successfully"

# @app.route("/contact")
# def get_contacts():
#     return "getting contact page"

if __name__ == "__main__":
    app.run(debug=True)     