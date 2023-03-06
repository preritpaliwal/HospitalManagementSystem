def format_sql(query):
    query = " ".join([line.strip() for line in query.splitlines()]).strip()
    return query

def Create_Tables(cursor):

    query = """
        CREATE TABLE IF NOT EXISTS 
        Login_Table (
            ID INT NOT NULL,
            Type VARCHAR(50) NOT NULL,
            Password VARCHAR(50) NOT NULL,

            PRIMARY KEY (ID)
        );

        CREATE TABLE IF NOT EXISTS
        Doctor (
            ID INT NOT NULL,
            Name VARCHAR(50) NOT NULL,
            Department VARCHAR(50) NOT NULL,
            Email VARCHAR(50) NOT NULL,
            Phone VARCHAR(10) NOT NULL,

            PRIMARY KEY (ID),
            FOREIGN KEY (ID) REFERENCES Login_Table(ID)
        );

        CREATE TABLE IF NOT EXISTS
        Room (
            Number VARCHAR(50) NOT NULL,
            Availibility INT NOT NULL,
            Capacity INT NOT NULL,

            PRIMARY KEY (Number)
        );

        CREATE TABLE IF NOT EXISTS
        Patient (
            ID INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(50) NOT NULL,
            Age INT NOT NULL,
            Phone VARCHAR(10) NOT NULL,
            Email VARCHAR(50) NOT NULL,
            Address VARCHAR(100) NOT NULL,
            InsuranceID VARCHAR(50),

            PRIMARY KEY (ID)
        );


        CREATE TABLE IF NOT EXISTS
        Test_Treatment (
            
            Code VARCHAR(50) NOT NULL,
            Name VARCHAR(50) NOT NULL,
            Cost INT NOT NULL,
            Type VARCHAR(10) NOT NULL,

            PRIMARY KEY (Code)
        );

        CREATE TABLE IF NOT EXISTS
        Undergoes (
            ID INT NOT NULL AUTO_INCREMENT,
            Code VARCHAR(50) NOT NULL, 
            Patient INT NOT NULL, 
            Doctor INT NOT NULL, 
            dt DATE, 
            slot INT, 
            Outcome VARCHAR(1024), 
            Image VARCHAR(256), 

            PRIMARY KEY (ID, Code, Patient, Doctor),
            FOREIGN KEY (Code) REFERENCES Test_Treatment(Code),
            FOREIGN KEY (Patient) REFERENCES Patient(ID),
            FOREIGN KEY (Doctor) REFERENCES Doctor(ID)

        );

        CREATE TABLE IF NOT EXISTS
        Appointment (
            ID INT NOT NULL AUTO_INCREMENT,
            Patient INT NOT NULL, 
            Doctor INT NOT NULL, 
            dt DATE NOT  NULL, 
            slot INT NOT NULL, 
            
            PRIMARY KEY (ID, Patient, Doctor),
            FOREIGN KEY (Patient) REFERENCES Patient(ID),
            FOREIGN KEY (Doctor) REFERENCES Doctor(ID)

        );

        CREATE TABLE IF NOT EXISTS
        Stay (
            ID INT NOT NULL AUTO_INCREMENT,
            Patient INT NOT NULL, 
            Room VARCHAR(50) NOT NULL, 
            admit DATE NOT NULL,
            discharge DATE , 

            PRIMARY KEY (ID, Patient, Room),
            FOREIGN KEY (Patient) REFERENCES Patient (ID),
            FOREIGN KEY (Room) REFERENCES Room (Number)
            
        );

        CREATE TABLE IF NOT EXISTS
        Medicine (
            ID INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(128) NOT NULL, 
            Manufacturer VARCHAR(128) NOT NULL, 
            Price INT NOT NULL, 

            PRIMARY KEY (ID)

        );

        CREATE TABLE IF NOT EXISTS
        Prescribes (
            ID INT NOT NULL AUTO_INCREMENT,
            Patient INT NOT NULL, 
            Doctor INT NOT NULL, 
            Medicine INT NOT NULL,
            Dosage VARCHAR (20) NOT NULL, 
            Duration INT NOT NULL, 
            dt DATE NOT NULL,

            PRIMARY KEY (ID, Patient, Medicine),
            FOREIGN KEY (Patient) REFERENCES Patient (ID),
            FOREIGN KEY (Medicine) REFERENCES Medicine (ID)
        );    
    """
    
    query = format_sql(query)
    
    # print(query)
    # cursor.execute(query)
    return query
    
def Initialise_Tables(cursor):
    
    query = """
    
    INSERT INTO Login_Table VALUES (1, 'Front Desk User', 'Vibhu');
    INSERT INTO Login_Table VALUES (2, 'Data Entry Operator','Prerit');
    INSERT INTO Login_Table VALUES (3, 'Doctor', 'Deepsikha');
    INSERT INTO Login_Table VALUES (4, 'Doctor', 'Anushka');
    INSERT INTO Login_Table VALUES (5, 'Admin', 'Umika');

    INSERT INTO Doctor VALUES (3, 'Deepsikha', 'Physician', 'Deepsikha@gmail.com', '1234567890');
    INSERT INTO Doctor VALUES (4, 'Anushka', 'Cardiology', 'Anushka@gmail.com', '1234554321');

    INSERT INTO Room VALUES ('A-101', 1, 1);
    INSERT INTO Room VALUES ('A-102', 1, 1);
    INSERT INTO Room VALUES ('A-103', 2, 3);
    INSERT INTO Room VALUES ('A-104', 3, 3);

    INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Vibhu', '1111111111', 'vibhuyadav41002@gmail.com', 'Addressssssss', '12345');
    INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Prerit', '1111111112', 'prerit@gmail.com', 'Addressssssss', '12346');
    INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Umika', '1111111113', 'umika@gmail.com', 'Addressssssss', '12347');

    INSERT INTO Test_Treatment VALUES ("ABC123", "Test1", 50000, "Test");
    INSERT INTO Test_Treatment VALUES ("ABC456", "Test2", 3000, "Test");
    INSERT INTO Test_Treatment VALUES ("ABC987", "Treatment1", 10000, "Treatment");
    INSERT INTO Test_Treatment VALUES ("ABC654", "Treatment2", 20000, "Treatment");

    INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ("ABC123", 1, 3, NULL, NULL, NULL, NULL);
    INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ("ABC456", 2, 3, NULL, NULL, NULL, NULL);
    INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ("ABC456", 2, 4, NULL, NULL, NULL, NULL);
    INSERT INTO Undergoes (Code, Patient, Doctor, dt, slot, outcome, Image) VALUES ("ABC654", 3, 4, NULL, NULL, NULL, NULL);

    INSERT INTO Appointment (Patient, Doctor, dt, slot) VALUES (1, 3, '2023-03-04', 1);
    INSERT INTO Appointment (Patient, Doctor, dt, slot) VALUES (2, 3, '2023-03-04', 2);
    INSERT INTO Appointment (Patient, Doctor, dt, slot) VALUES (2, 4, '2023-03-04', 3);
    INSERT INTO Appointment (Patient, Doctor, dt, slot) VALUES (3, 4, '2023-03-04', 1);\

    INSERT INTO Stay (Patient, Room, admit, discharge) VALUES (1, 'A-101', '2023-03-04', '2023-03-05');
    INSERT INTO Stay (Patient, Room, admit, discharge) VALUES (2, 'A-102', '2023-03-04', '2023-03-05');
    INSERT INTO Stay (Patient, Room, admit, discharge) VALUES (3, 'A-103', '2023-03-04', '2023-03-05');

    INSERT INTO Medicine (Name, Manufacturer, Price) VALUES ('Paracetamol', 'Cipla', 20);
    INSERT INTO Medicine (Name, Manufacturer, Price) VALUES ('Azithromycin', 'Sun Pharma', 50);
    INSERT INTO Medicine (Name, Manufacturer, Price) VALUES ('Cetrizine', 'Cipla', 10);

    INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (1, 3, '1-1-0' , 5 , '2023-03-04');
    INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (2, 1, '1-0-0' , 5 , '2023-03-04');
    INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (2, 2, '1-0-0' , 5 , '2023-03-04');
    INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (3, 1, '1-0-0' , 5 , '2023-03-04'); 
    """
    
    query = format_sql(query)
    
def Drop_Tables(cursor):

    query = """
        DROP TABLE IF EXISTS Undergoes;
        DROP TABLE IF EXISTS Appointment;
        DROP TABLE IF EXISTS Stay;
        DROP TABLE IF EXISTS Prescribes;
        DROP TABLE IF EXISTS Medicine;
        DROP TABLE IF EXISTS Room;
        DROP TABLE IF EXISTS Test_Treatment;
        DROP TABLE IF EXISTS Patient;
        DROP TABLE IF EXISTS Doctor;
        DROP TABLE IF EXISTS Login_Table;
    """
    
    
    query = format_sql(query)

    return query
    # cursor.execute(query)
    
