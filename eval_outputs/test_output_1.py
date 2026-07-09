[PYTHON]
import sqlite3

def get_user_data(user_id):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()