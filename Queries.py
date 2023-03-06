import paramiko
import pymysql
from tabulate import tabulate

def setup_Database():
    # Open SSH connection to the server

    print("Connecting to SSH...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.5.18.70', username='20CS10072', password='bt20')

    print("Connecting to Database...")

    # Open database connection
    connection = pymysql.connect(
        host='10.5.18.70',
        user='20CS10072',
        password='20CS10072',
        db='20CS10072',
        autocommit= True
    )

    print("Connected to Database")

    return (ssh, connection)

def close_Database(ssh, connection):
    # Close database connection
    connection.close()

    # Close SSH connection
    ssh.close()