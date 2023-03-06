
# def update_result(cursor, TTCode, PatientID, DoctorID, date, slot, outcome, image):
def update_result(cursor, UndergoesID, outcome, image = None):
    """
    Update the outcome and/or image of a Test or Treatment in the Undergoes Table
    """
    # TODO - Check if outcome has already been filled
    
    query = f"SELECT * FROM Undergoes WHERE ID = {UndergoesID};"
    cursor.execute(query)
    
    if(cursor.rowcount == 0):
      print("Test / Treatment Session not created.")
      return False
    
    if(outcome is not None):
        query = f"UPDATE Undergoes \
          SET outcome = '{outcome}' \
          WHERE ID = {UndergoesID}"

        cursor.execute(query)
        
    if (image is not None):
        query = f"UPDATE Undergoes \
          SET image = '{image}' \
          WHERE ID = {UndergoesID}"
          
        cursor.execute(query)
        
    return True