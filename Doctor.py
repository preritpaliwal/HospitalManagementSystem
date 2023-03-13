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

def fetch_schedule(cursor, DoctorID):
    
    slots = [ str(x)+":00-"+str(x+1)+":00" for x in range(9,13) ] + [ str(x)+":00-"+str(x+1)+":00" for x in range(14,18) ]
    
    query = f"SELECT dt,slot,'Appointment' FROM Appointment WHERE Doctor = {DoctorID} ORDER BY dt, Slot;"
    cursor.execute(query)
    
    
    appointments = list(cursor.fetchall())
    
    for i,ele in enumerate(appointments):
        appointments[i] = (ele[0], slots[ele[1]-1], "Appointment", "")
    
    print(appointments)
    
    query = f"SELECT Undergoes.dt, Undergoes.slot,Test_Treatment.Type, Test_Treatment.Name  FROM Undergoes JOIN Test_Treatment on (Undergoes.Code = Test_Treatment.Code) WHERE Doctor = {DoctorID} and dt is NOT NULL ORDER BY dt, Slot;"
    cursor.execute(query)
    
    tests_treatments = list(cursor.fetchall())
    
    for i,ele in enumerate(tests_treatments):
        tests_treatments[i] = (ele[0], slots[ele[1]-1], ele[2], ele[3])
    
    print(tests_treatments)
    
    schedule = appointments + tests_treatments
    
    return schedule
    
    

def patient_history_TT(cursor, PatientID):
    """
    Fetch Test / Treatment history of a patient.
    Returns Patient's Name, 
    """
    
    query = f"SELECT Patient.Name, Doctor.Name, Test_Treatment.Name, Undergoes.dt, Undergoes.Slot, Undergoes.Outcome, Undergoes.Image \
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
