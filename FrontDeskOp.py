import pymysql
from tabulate import tabulate
from flask_mail import Message

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
    print(tabulate(rows, headers=columns, tablefmt='psql'))

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
        print(cursor.fetchall())
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
# TODO -


def schedule_appointment(cursor, PatientID, DoctorID, Date):

    query = f"SELECT * FROM Patient WHERE ID = {PatientID};"
    cursor.execute(query)

    # Case when the patient isn't registered
    if (cursor.rowcount == 0):
        return (1,None,None)

    query = f"SELECT * FROM Doctor WHERE ID = {DoctorID};"
    cursor.execute(query)

    # Case when Doctor isn't registered
    if (cursor.rowcount == 0):
        return (2,None,None)

    if (Date is None or Date == ""):
        Date = 'CURDATE()'
    else:
        Date = "'" + Date + "'"

    # OR operator is used and we can't use slots where "either" Patient or Doctor has an appointment.
    query = f"SELECT * FROM Appointment \
            WHERE (Patient = {PatientID} or Doctor = {DoctorID}) and dt = {Date};"

    cursor.execute(query)

    # We assume a doctor has 8 total slots (1 hr each) per day (9 am - 1 pm, 2 pm - 6 pm)
    if (cursor.rowcount == 8):
        return (3,None,None)

    rows = cursor.fetchall()

    # 1 : available slot
    # slots = [("Slot " + str(x), 1) for x in range(1, 9)]
    slots = [ (str(x)+":00-"+str(x+1)+":00", 1) for x in range(9,13) ] + [ (str(x)+":00-"+str(x+1)+":00",1) for x in range(14,18) ]
    for row in rows:
        slots[(int)(row[4]-1)] = (slots[(int)(row[4]-1)][0], 0)

    query = f"INSERT INTO Appointment (Patient, Doctor, dt, slot) VALUES ({PatientID}, {DoctorID}, {Date}, -1);"
    cursor.execute(query)

    # query = "SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_name = 'Appointment';"
    query = f"SELECT ID FROM Appointment WHERE (Patient = {PatientID} and Doctor = {DoctorID} and dt = {Date} and slot = -1);"
    cursor.execute(query)

    # Get the next available appointment ID
    app_ID = cursor.fetchall()[0][0]

    return (0, slots, app_ID)

def update_appointment_slot(cursor, app_ID, slot):

    query = f"UPDATE Appointment SET slot = {slot} WHERE ID = {app_ID};"
    cursor.execute(query)

    if (cursor.rowcount == 0):
        print("Appointment doesn't exist! for ID = ", app_ID)
        return None

    query = f"SELECT Patient.ID, Patient.Name, Doctor.ID, Doctor.Name, Appointment.dt, Appointment.Slot \
            FROM Appointment JOIN Patient JOIN Doctor ON (Appointment.Patient = Patient.ID and Appointment.Doctor = Doctor.ID) \
            WHERE Appointment.ID = {app_ID};"
    cursor.execute(query)

    app_data = cursor.fetchall()[0]
    
    slots = [ str(x)+":00-"+str(x+1)+":00" for x in range(9,13) ] + [ str(x)+":00-"+str(x+1)+":00" for x in range(14,18) ]
    app_data = (app_data[0], app_data[1], app_data[2], app_data[3], app_data[4], slots[app_data[5]-1] )
    
    return app_data

# Notify Doctors of Appointments
# TODO - Figure out this shit
def email_doctor(cursor, mail, app_ID = None, TT_id = None):
    
    slots = [ str(x)+":00-"+str(x+1)+":00" for x in range(9,13) ] + [ str(x)+":00-"+str(x+1)+":00" for x in range(14,18) ]
    
    if(app_ID is not None):
        
        query = f"SELECT Patient.Name, Doctor.Name, Doctor.Email, Appointment.dt, Appointment.Slot \
                FROM Appointment JOIN Patient JOIN Doctor ON (Appointment.Patient = Patient.ID and Appointment.Doctor = Doctor.ID) \
                WHERE Appointment.ID = {app_ID};"
        cursor.execute(query)
        app_rows = cursor.fetchall()        
        
        app_patient = app_rows[0][0]
        doctor_name = app_rows[0][1]
        doctor_email = app_rows[0][2]
        app_date = app_rows[0][3]
        app_slot = slots[app_rows[0][4] - 1]        
        
        email = Message(
            subject= f'Appointment scheduled on {app_date} at {app_slot}',
            sender = 'medpal.hospital@gmail.com',
            recipients= [doctor_email],
            
            body = f"Hello Dr. {doctor_name},\n\n \
                You have an appointment with patient : {app_patient} on {app_date} at {app_slot}.\n\n"
        ) 
        
        # print(email)
        
        try:
            print(f"Sending email to {doctor_email}")
            
            mail.send(email)
            
            print("Email sent successfully!")
            
        except Exception as e:
            print(f"\n\nMAIL WAS NOT SENT : {e}\n\n")
        

# TODO - Take User opinion for room type, Currently assigning room with most availability %.


def admit_patient(cursor, ID, AdmitDate):
    """
    Admit a Patient to the hospital and assign a room to them.
    Returns the room number assigned to the patient, 'None' if no rooms are available.
    """

    query = f"SELECT * FROM Room WHERE Availibility > 0 ORDER BY (Availibility / Capacity ) DESC, Capacity ASC;"

    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate( rows, headers = columns, tablefmt= 'psql') )

    if (cursor.rowcount == 0):
        print("No Rooms Available")
        return False

    RoomNo = rows[0][0]

    update = f"UPDATE Room SET Availibility = Availibility - 1 WHERE Number = '{RoomNo}' AND Availibility > 0"
    cursor.execute(update)

    print(f"Patient : {ID} has been assigned to Room {RoomNo}")

    if AdmitDate is None or AdmitDate == "":
        AdmitDate = "CURDATE()"
    else:
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

    if (cursor.rowcount == 0):
        print("Patient isn't Admitted!")
        return False

    query = f"SELECT * FROM Stay WHERE Patient = {PatientID} and discharge IS NOT NULL;"
    cursor.execute(query)

    if (cursor.rowcount != 0):
        print("Patient Already Discharged!")
        return False

    query = f"SELECT * FROM Stay WHERE Patient = {PatientID};"
    cursor.execute(query)

    RoomNo = cursor.fetchall()[0][2]

    query = f"UPDATE Room SET Availibility = Availibility + 1 WHERE Number = '{RoomNo}' and Availibility < Capacity;"
    cursor.execute(query)

    if (cursor.rowcount == 0):
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
def schedule_TT(cursor, PatientID, DoctorID, TestID, Date):
    
    query = f"SELECT * FROM Undergoes \
            WHERE Patient = {PatientID} and Doctor = {DoctorID} and Code = '{TestID}' and dt is NULL and slot is NULL;"

    cursor.execute(query)
    
    if(cursor.rowcount == 0):
        print("No such Test/Treatment prescribed to the patient")
    
    rows = cursor.fetchall()
    
    first_row = rows[0]
    app_ID = first_row[0]
    
    if (Date is None or Date == ""):
        Date = "CURDATE()"
    else:
        Date = "'" + Date + "'"
    
    query = f"SELECT * FROM Appointment \
        WHERE (Patient = {PatientID} or Doctor = {DoctorID}) and dt = {Date};"    
    cursor.execute(query)
    
    # We assume a doctor has 8 total slots (1 hr each) per day (9 am - 1 pm, 2 pm - 6 pm)
    if (cursor.rowcount == 8):
        return -1

    rows = cursor.fetchall()

    # 1 : available slot
    # slots = [("Slot " + str(x), 1) for x in range(1, 9)]
    slots = [ (str(x)+":00-"+str(x+1)+":00", 1) for x in range(9,13) ] + [ (str(x)+":00-"+str(x+1)+":00",1) for x in range(14,18) ]
    for row in rows:
        slots[(int)(row[4]-1)] = (slots[(int)(row[4]-1)][0], 0)
    
    idx = -1
    for (i,(slot, avail)) in enumerate(slots):
        if(avail == 1):
            idx = i+1
            break
        
    if(idx == -1):
        return -1
    
    query =f"UPDATE Undergoes SET dt = {Date}, slot = {idx} WHERE ID = {app_ID};"
    
    cursor.execute(query)
    
    return idx

def unscheduled_TT(cursor):

    query = "SELECT Patient.ID, Patient.Name, Test_Treatment.Code, Test_Treatment.Name, Doctor.ID, Doctor.Name  \
            FROM Undergoes join Patient join Doctor join Test_Treatment \
            on (Undergoes.Patient = Patient.ID and Undergoes.Doctor = Doctor.ID and Undergoes.Code = Test_Treatment.Code) \
            WHERE Undergoes.dt is NULL and Undergoes.slot is NULL;"

    cursor.execute(query)

    rows = cursor.fetchall()

    return rows
