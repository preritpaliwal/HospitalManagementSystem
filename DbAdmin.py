import pymysql

def fetch_users(cursor):
    query = "SELECT ID as Username, Type FROM Login_Table;"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    return rows
    

def add_user(cursor, ID, Type, Password):
    """
    Add a new user to the Database (Login_Table).
    Returns a boolean False if a user with exact same credentials exists.
    Returns True on success.
    """
    
    query = f"SELECT * FROM Login_Table WHERE ID = '{ID}' and Type = '{Type}' and Password = '{Password}'; "
    cursor.execute(query)
    
    if(cursor.rowcount != 0):
        return False
    
    query = f"INSERT INTO Login_Table VALUES ( {ID}, '{Type}', '{Password}' );"
    
    try:
        cursor.execute(query)
    except pymysql.Error as err:
        print(err)
        print("User exists, primary key match.")
        return False    
    
    return True

def delete_user(cursor, ID):
    """
    Delete a User with given ID.
    """
    
    query = f"SELECT * FROM Login_Table WHERE ID = {ID};"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(rows, type(rows))
    print(rows[0], type(rows[0]))
    
    user_type = rows[0][1]
    
    if(user_type == "Database Administrator"):
        print("Cannot delete Admin user.")
        return
    
    if(user_type == "Doctor"):
        query = f"DELETE FROM Doctor WHERE ID = {ID};"
        cursor.execute(query)
        
    
    query = f"DELETE FROM Login_Table WHERE ID = {ID};"
    cursor.execute(query)

#TODO - Implement Data Security with suitable access control
