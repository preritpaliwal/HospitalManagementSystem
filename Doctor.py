
def fetch_all_patients(cursor, DoctorID, PatientID):
    
    query = f"SELECT * \
            FROM Undergoes JOIN Patient on (Undergoes.Patient = Patient.ID) \
            WHERE Doctor = {DoctorID};"
    
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate( rows, headers = columns, tablefmt= 'psql') )
    
    return (columns, rows)

# TODO - Exaclty what info do we want to show here?
def query_patient_info(cursor, DoctorID, PatientID):

    query = f"SELECT * \
          FROM Undergoes JOIN Patient on (Undergoes.Patient = Patient.ID) \
          WHERE Doctor = {DoctorID} and Patient = {PatientID};"
          
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate( rows, headers = columns, tablefmt= 'psql') )
    
    return (columns, rows)


def prescribe_test_treatment(cursor, TTCode, DoctorID, PatientID):
    """
    Prescribe Tests and Treatments to Patients 
    Date, Slot, Outcome and Image aren't entered by doctor. Hence they are NULL
    """

    query = f"INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ( '{TTCode}', {PatientID}, {DoctorID}, NULL, NULL, NULL, NULL ) "
    cursor.execute(query)

# TODO - Implement this feature


def prescribe_medicine(cursor, DoctorID, PatientID, MedicineID, Dosage, Duration):
    """
    Prescribe a Medicine to a Patient.
    Dosage should of be form '<Morning>-<Noon>-<Evening>'
    Duration is currently a Integer.
    Duration can be in Days(D), Weeks(W), Months(M) with form "<Value><Code>".
    """

    query = f"INSERT INTO Prescribes (Patient, Doctor, Medicine, Dosage, Duration, dt) VALUES \
                                ( {PatientID}, {DoctorID}, {MedicineID}, '{Dosage}',{Duration}, CURDATE() );"

    cursor.execute(query)

# Send Email to doctor on a weekly basis with all the patients treated by the doctor
# Implement High Priority Notifications for patients with critical conditions
# TODO - Figure out this shit
