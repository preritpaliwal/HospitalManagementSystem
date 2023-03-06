
def update_result(cursor, TTCode, PatientID, DoctorID, date, slot, outcome, image):
    """
    Update the outcome and/or image of a Test or Treatment in the Undergoes Table.
    """
    
    if(outcome is not None):
        query = f"UPDATE Undergoes \
          SET outcome = '{outcome}' \
          WHERE Code = {TTCode} and Patient = '{PatientID}' and Doctor = {DoctorID} and dt = '{date}' and slot = '{slot} "

        cursor.execute(query)
        
    if (image is not None):
        query = f"UPDATE Undergoes \
          SET image = '{image}' \
          WHERE Code = {TTCode} and Patient = '{PatientID}' and Doctor = {DoctorID} and dt = '{date}' and slot = '{slot} "

        cursor.execute(query)