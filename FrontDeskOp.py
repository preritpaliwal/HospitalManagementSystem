import pymysql
from tabulate import tabulate

def validate_user(cursor, Id, Type, Password):
    """
    Check if the user exists in the database.
    Returns boolean false if the user doesn't exist, else returns true.
    """
    
    query = f"SELECT * \
          FROM Login_Table \
          WHERE ID = '{Id}' and Type = '{Type}' and Password = '{Password}'; "
          
    print(query)

    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    print( tabulate(rows , headers = columns, tablefmt= 'psql' ) )

    if (Id, Type, Password) in rows:
        print("Match Found")
        return True
    return False

def register_patient(cursor, Name, Age, Phone, Email, Address, InsuranceID):
    """
    Register a new patient in the database.
    If the patient already exists, return False.
    """
    
    query = f"SELECT * FROM Patient WHERE Name = '{Name}' and Age = '{Age}' and Phone = '{Phone}' "
    cursor.execute(query)

    if (cursor.rowcount != 0):
        print("Patient already exists.")
        return False

    query = f"INSERT INTO Patient ( Name, Age, Phone, Email, Address, InsuranceID ) VALUES {Name, Age, Phone, Email, Address, InsuranceID} ;"
    
    try:
        cursor.execute(query)
    except pymysql.Error as err:
        print(err)
        print("User exists, primary key match.")
        return False

    return True

# Schedule Appointments for Patients
# TODO - Figure out this shit

# Notify Doctors of Appointments
# TODO - Figure out this shit

# TODO - Take User opinion for room type, Currently assigning room with most availability %.
def admit_patient (cursor, ID, AdmitDate):
    """
    Admit a Patient to the hospital and assign a room to them.
    Returns the room number assigned to the patient, 'None' if no rooms are available.
    """
    
    query = f"SELECT * FROM Room WHERE Availibility > 0 ORDER BY (Availibility / Capacity ) DESC, Capacity ASC;"

    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate( rows, headers = columns, tablefmt= 'psql') )
    
    if(cursor.rowcount == 0):
        print("No Rooms Available")
        return False
    
    RoomNo = rows[0][0]
    
    update = f"UPDATE Room SET Availibility = Availibility - 1 WHERE Number = '{RoomNo}' AND Availibility > 0";    
    cursor.execute(update)
    
    print(f"Patient : {ID} has been assigned to Room {RoomNo}")
    
    if AdmitDate is None or AdmitDate == "":
        AdmitDate = "CURDATE()"
    else :
        AdmitDate = "'" + AdmitDate + "'" 
        
    stay_query = f"INSERT INTO Stay (Patient, Room , admit, discharge) VALUES ( {ID}, '{RoomNo}', {AdmitDate}, NULL);"
    print(stay_query)
    try:
        cursor.execute(stay_query)
    except pymysql.Error as err:
        print(err)
        print("User exists, primary key match.")
        return False
    
    return True

def discharge_patient(cursor, PatientID, DischargeDate):
    """
    Discharge a Patient and update the Room's Availibility and Patient's Stay details.
    """
        
    query = f"SELECT * FROM Stay WHERE Patient = {PatientID};"
    cursor.execute(query)
    
    if(cursor.rowcount == 0):
        print("Patient isn't Admitted!")
        return False
    
    query = f"SELECT * FROM Stay WHERE Patient = {PatientID} and discharge IS NOT NULL;"
    cursor.execute(query)
    
    if(cursor.rowcount != 0):
        print("Patient Already Discharged!")
        return False
    
    query = f"SELECT * FROM Stay WHERE Patient = {PatientID};"
    cursor.execute(query)
    
    RoomNo = cursor.fetchall()[0][2]
    
    query = f"UPDATE Room SET Availibility = Availibility + 1 WHERE Number = '{RoomNo}' and Availibility < Capacity;"
    cursor.execute(query)
    
    if(cursor.rowcount == 0):
        print("Room Already empty")
        return False
    
    if DischargeDate is None or DischargeDate == "":
        DischargeDate = "CURDATE()"
    else:
        DischargeDate = "'" + DischargeDate + "'"
    
    stay_query = f"UPDATE Stay SET discharge = {DischargeDate} WHERE Patient = {PatientID} AND discharge IS NULL;"
    cursor.execute(stay_query)
    
    return True

# Schedule Tests and Treatments Sessions prescribed to Patients by Doctors
# TODO - Figure out this shit
def unscheduled_TT(cursor):
    
    query = "SELECT Patient.ID, Patient.Name, Test_Treatment.Code, Test_Treatment.Name, Doctor.ID, Doctor.Name  \
            FROM Undergoes join Patient join Doctor join Test_Treatment \
            on (Undergoes.Patient = Patient.ID and Undergoes.Doctor = Doctor.ID and Undergoes.Code = Test_Treatment.Code)  ;"
    
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    return rows
        