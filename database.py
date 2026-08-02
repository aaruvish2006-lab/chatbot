def connect_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",      # Change this if your MySQL password is different
        database="chatbot"
    )
    return db