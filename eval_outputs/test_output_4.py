[PYTHON]
import mysql.connector

def connect_secure_production_db(database, username, password):
    # Enable SSL and require secure connection
    ssl_params = {
        'ssl_ca': '/path/to/ca.pem',
        'ssl_cert': '/path/to/client-cert.pem',
        'ssl_key': '/path/to/client-key.pem',
        'ssl_verify_cert': True,
    }
    return mysql.connector.connect(
        database=database,
        user=username,
        password=password,
        host='localhost',  # Change to your production host
        port=3306,  # Change to your production port
        ssl_enabled=True,
        **ssl_params
    )

# Example usage:
database = 'mydatabase