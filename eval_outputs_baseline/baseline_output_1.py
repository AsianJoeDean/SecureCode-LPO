import sqlite3

def get_user_data(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    return data