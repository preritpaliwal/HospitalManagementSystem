# TODO - Show medications prescribed by doctor
def fetch_all_patients(cursor, DoctorID):
    
    query = f"SELECT DISTINCT Patient.ID, Patient.Name, Patient.Age,  Patient.Phone, \
            Patient.Email , Patient.Address , Patient.InsuranceID  \
            FROM Undergoes JOIN Patient on (Undergoes.Patient = Patient.ID) \
            WHERE Doctor = {DoctorID};"
    
    cursor.execute(query)
    
    # columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate( rows, headers = columns, tablefmt= 'psql') )
    
    return rows

# TODO - Implement two functions to show patient details
# 1. Tests => (Patient.Name, Test.Name, Doctor.Name, Date, Slot, Outcome)
# 2. Medication => (Patient.Name, Doctor.Name, Medication.Name, Dosage, Duration, Date)
def patient_history_TT(cursor, PatientID):
    """
    Fetch Test / Treatment history of a patient.
    Returns Patient's Name, 
    """
    
    query = f"SELECT Patient.Name, Doctor.Name, Test_Treatment.Name, Undergoes.dt, Undergoes.Slot, Undergoes.Outcome \
            FROM Patient JOIN Undergoes JOIN Doctor JOIN Test_Treatment \
            on (Undergoes.Patient = Patient.ID and Undergoes.Doctor = Doctor.ID and Undergoes.Code = Test_Treatment.Code) \
            WHERE Patient.ID = {PatientID};"
            
    cursor.execute(query)
    rows = cursor.fetchall()
    
    return rows

def patient_history_Medication(cursor, PatientID):
    
    query = f"SELECT Patient.Name, Doctor.Name, Medicine.Name, Medicine.Manufacturer, Prescribes.Dosage, Prescribes.Duration, Prescribes.dt \
            FROM Prescribes JOIN Patient JOIN Doctor JOIN Medicine \
            on ( Prescribes.Patient = Patient.ID and Prescribes.Doctor = Doctor.ID and Prescribes.Medicine = Medicine.ID ) \
            WHERE Patient.ID = {PatientID};"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    return rows

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

def prescribe_medicine(cursor, DoctorID, PatientID, MedicineID, Dosage, Duration, Date):
    """
    Prescribe a Medicine to a Patient.
    Dosage should of be form '<Morning>-<Noon>-<Evening>'
    Duration is currently a Integer.
    Duration can be in Days(D), Weeks(W), Months(M) with form "<Value><Code>".
    """
    
    if Date is None or Date == "":
        Date = "CURDATE()"
    else:
        Date = "'" + Date + "'"

    query = f"INSERT INTO Prescribes (Patient, Doctor, Medicine, Dosage, Duration, dt) VALUES \
                                ( {PatientID}, {DoctorID}, {MedicineID}, '{Dosage}',{Duration}, {Date} );"


    cursor.execute(query)

# Send Email to doctor on a weekly basis with all the patients treated by the doctor
# Implement High Priority Notifications for patients with critical conditions
# TODO - Figure out this shit
