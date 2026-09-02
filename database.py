import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="flask_student_db"
    )

    return connection


if __name__ == "__main__":
    connection = get_db_connection()

    if connection.is_connected():
        print("Database connected successfully")

    connection.close()