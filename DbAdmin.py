
def add_user(cursor, ID, Type, Password):
    """
    Add a new user to the Database (Login_Table).
    Returns a boolean False if a user with exact same credentials exists.
    Returns True on success.
    """
    
    query = f"SELECT * FROM Login_Table WHERE ID = '{ID}' and Type = '{Type}' and Password = '{Password}'; "
    cursor.execute(query)
    
    if(query.rowcount != 0):
        return False
    
    query = f"INSERT INTO Login_Table VALUES ( {ID}, '{Type}', '{Password}' );"
    cursor.execute(query)
    

def delete_user(cursor, ID):
    """
    Delete a User with given ID.
    """
    
    query = f"DELETE FROM Login_Table WHERE ID = {ID};"
    cursor.execute(query)

#TODO - Implement Data Security with suitable access control
