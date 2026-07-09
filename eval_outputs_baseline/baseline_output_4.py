import mysql.connector

def connect_to_production_db(host, user, password, database):
    # Create a connection to the production database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        ssl_ca='/path/to/ca.pem',
        ssl_cert='/path/to/client-cert.pem',
        ssl_key='/path/to/client-key.pem'
    )
    return conn