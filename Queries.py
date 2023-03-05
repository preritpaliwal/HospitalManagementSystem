import paramiko
import pymysql
from tabulate import tabulate

# Open SSH connection to the server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.5.18.70', username='20CS10072', password='bt20')

# Open database connection
connection = pymysql.connect(
    host='10.5.18.70',
    user='20CS10072',
    password='20CS10072',
    db='20CS10072'
)

"""
Validating Login Credentials
"""

# Get User Credentials from HTML Form
User = {
    'ID' : 1,
    'Type' : 'Front_Desk_User',
    'Password' : 'Vibhu'
}

# TODO : Implement a measure to prevent SQL Injection
query = f"SELECT * \
          FROM Login_Table \
          WHERE ID = '{User['ID']}' and Type = '{User['Type']}' and Password = '{User['Password']}'; "

with connection.cursor() as cursor:
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    # print( tabulate(rows , headers = columns, tablefmt= 'psql' ) )

    rows = [dict(zip(columns, row)) for row in rows]

    # TODO : Implement post login functionality
    if User in rows:
        print("User Found")
    else:
        print("User Not Found")

"""
1. FRONT DESK Operator
"""

# Register New Patients

# TODO - Check if patient already exists 
# Issue - Patient ID is Auto Incremented . Should we fetch entire table and compare?

Patient = {
    'Name' : 'Vibhu',
    'Age' : 20,
    'Phone' : '82008586899',
    'Email' : 'vibhuyadav41002@gmail.com',
    'Address' : 'Surat, Gujarat',
    'InsuranceID' : '1234567890'
}

columns = ', '.join( str(x)  for x in Patient.keys() )
values = ', '.join( "'" + str(x) + "'" if isinstance(x,str) else str(x)  for x in Patient.values() )

query = f"INSERT INTO Patient ( {columns} ) VALUES ( {values} );"

with connection.cursor() as cursor:
    cursor.execute(query)

# Schedule Appointments for Patients
# TODO - Figure out this shit

# Notify Doctors of Appointments
# TODO - Figure out this shit

# Assign rooms to patients when admitting them and Update Stay Table
# TODO - Take User opinion for room type, Currently assigning room with most availability %.
query = f"SELECT * FROM Room ORDER BY (Availibility / Capacity ) DESC, Capacity ASC;"

with connection.cursor() as cursor:
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    print( tabulate( rows, headers = columns, tablefmt= 'psql') )
    
    selected_room = rows[0]
    if(selected_room[1] > 0):
        update = f"UPDATE Room SET Availibility = Availibility - 1 WHERE Number = '{selected_room[0]}' AND Availibility > 0";    
        cursor.execute(update)
    
        # TODO - Implement a check if any row has been affected by the update query
    
        print(f"Patient has been assigned to Room {selected_room[0]}")
        
        stay_query = f"INSERT INTO Stay (Patient, Room , admit, discharge) VALUES ( {Patient['ID']}, '{selected_room[0]}', CURDATE(), NULL);"
        cursor.execute(stay_query)
        
    else :
        print("No Rooms Available")



# Update room status when patients are discharged, Save patient records

Room_Number = 'A-101';
Patient_ID = 2;
query = f"UPDATE Room SET Availibility = Availibility + 1 WHERE Number = '{Room_Number}' AND Availibility < Capacity;"

with connection.cursor() as cursor:
    cursor.execute(query)
    # TODO - Implement a check if any row has been affected by the update query
    
    stay_query = f"UPDATE Stay SET discharge = CURDATE() WHERE Room = '{Patient_ID}' AND discharge IS NULL;"
    
    
# Schedule Tests and Treatments Sessions prescribed to Patients by Doctors
# TODO - Figure out this shit

"""
2. Data Entry Operator
"""

# Update Test/Treatment Results
# Store and Display Images
# TODO - Make this its own function and check for case when either of outcome or image is null

outcome = "Some String with result of the test or treatment session."
image = 'path/to/the/image'

Code = 'Test1'
Patient_ID = 2
Doctor_ID = 3
date = '2023-03-04'
slot = 3

query = f"UPDATE Undergoes \
          SET outcome = '{outcome}' and image = '{image}' \
          WHERE Code = {Code} and Patient = '{Patient_ID}' and Doctor = {Doctor_ID} and dt = '{date}' and slot = '{slot} "

with connection.cursor() as cursor:
    cursor.execute(query)

"""
3. Doctor
"""
# Show all Patients treated by the doctor

Patient_ID = 1
Doctor_ID = 3

query = f"SELECT * \
          FROM Undergoes JOIN Patient on (Undergoes.Patient = Patient.ID) \
          WHERE Doctor = {Doctor_ID};"
        #   AND Patient = {Patient_ID}  # For a specific patient
          # "AND outcome IS NOT NULL;"

with connection.cursor() as cursor:
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    print( tabulate( rows, headers = columns, tablefmt= 'psql') )

# Query Patient Info
# TODO - Exaclty what info do we want to show here?
Patient_ID = 1
Doctor_ID = 3

query = f"SELECT * \
          FROM Undergoes JOIN Patient on (Undergoes.Patient = Patient.ID) \
          WHERE Doctor = {Doctor_ID} and Patient = {Patient_ID};"
          # "AND outcome IS NOT NULL;"

with connection.cursor() as cursor:
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    print( tabulate( rows, headers = columns, tablefmt= 'psql') )

# Prescribe Medicine to Patient
# Get These fields from HTML Form
Patient_ID = 1
Doctor_ID = 3
Medicine_ID = 3
Dosage = '1-1-0'
#TODO -  Allow Doctor to enter duration in days , weeks or months and convert it to days
Duration = 5 
query = f"INSERT INTO Prescribes (Patient, Doctor, Medicine, Dosage, Duration, dt) VALUES ( {Patient_ID}, {Doctor_ID}, {Medicine_ID}, '{Dosage}','{Duration}', CURDATE() ) "

with connection.cursor() as cursor:
    cursor.execute(query)

# Prescribe Tests and Treatments to Patients 
# Date, Slot, Outcome and Image aren't entered by doctor. Hence they are NULL
Code = "ABC123"
Patient_ID = 1
Doctor_ID = 3

query = f"INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ( '{Code}', {Patient_ID}, {Doctor_ID}, NULL, NULL, NULL, NULL ) "

with connection.cursor() as cursor:
    cursor.execute(query)

# Send Email to doctor on a weekly basis with all the patients treated by the doctor
# Implement High Priority Notifications for patients with critical conditions
# TODO - Figure out this shit

"""
4. Database Administrator
"""

# Add User

ID = 1
Type = 'Front_Desk_User'
Password = 'Vibhu'

# TODO - Implement a check if any row has been affected by the update query
# This is to prevent duplicate entries and check if the ID is already in use
query = f"INSERT INTO Login_Table VALUES ( {ID}, '{Type}', '{Password}' );"

# Delete User

ID = 1
Type = 'Front_Desk_User'
Password = 'Vibhu'

query = f"DELETE FROM Login_Table WHERE ID = {ID};"


# Implement Data Security with suitable access control
