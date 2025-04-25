import mysql.connector

def get_db_connection():
    # print("Connecting to MySQL...")
    db = mysql.connector.connect(
        host="#",
        user="#",
        password="#",
        database="#"
    )
    # print("Connected to database:", db.database)
    return db