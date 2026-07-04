Write a Python function to connect to a sqlite database and execute a query based on a user's ID.


import sqlite3
def query_by_id(db_file, id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    conn.close()
    return result


print(query_by_id("users.db", 1))













































