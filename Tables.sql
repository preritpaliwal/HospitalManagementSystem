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
    Code VARCHAR(50) NOT NULL, -- Test_Treatment Code
    Patient INT NOT NULL, -- Patient ID
    Doctor INT NOT NULL, -- Doctor ID
    dt DATE, -- Nullable date (Doctor sets as NULL), FD user updates when scheduling
    slot INT, -- Slot of date when appointment is scheduled
    Outcome VARCHAR(1024), -- Test / Treatment Result
    Image VARCHAR(256), -- Image Path on Device

    PRIMARY KEY (ID, Code, Patient, Doctor),
    FOREIGN KEY (Code) REFERENCES Test_Treatment(Code),
    FOREIGN KEY (Patient) REFERENCES Patient(ID),
    FOREIGN KEY (Doctor) REFERENCES Doctor(ID)

);

CREATE TABLE IF NOT EXISTS
Appointment (
    ID INT NOT NULL AUTO_INCREMENT,
    Patient INT NOT NULL, -- Patient ID
    Doctor INT NOT NULL, -- Doctor ID
    dt DATE NOT  NULL, -- Date of Appointment
    slot INT NOT NULL, -- Slot of Chosen Date
    
    PRIMARY KEY (ID, Patient, Doctor),
    FOREIGN KEY (Patient) REFERENCES Patient(ID),
    FOREIGN KEY (Doctor) REFERENCES Doctor(ID)

);

CREATE TABLE IF NOT EXISTS
Stay (
    ID INT NOT NULL AUTO_INCREMENT,
    Patient INT NOT NULL, -- Patient ID
    Room VARCHAR(50) NOT NULL, -- Room Number
    admit DATE NOT NULL,
    discharge DATE , -- Nullable. NOT NULL value indicates patient has been discharged

    PRIMARY KEY (ID, Patient, Room),
    FOREIGN KEY (Patient) REFERENCES Patient (ID),
    FOREIGN KEY (Room) REFERENCES Room (Number)
    
);

CREATE TABLE IF NOT EXISTS
Medicine (
    ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(128) NOT NULL, -- Name of Medicine 
    Manufacturer VARCHAR(128) NOT NULL, -- Medicine Manufacturer
    Price INT NOT NULL, -- Price of Medicine

    PRIMARY KEY (ID)

);

CREATE TABLE IF NOT EXISTS
Prescribes (
    ID INT NOT NULL AUTO_INCREMENT,
    Patient INT NOT NULL, -- Patient ID
    Doctor INT NOT NULL, -- To be Updated in MYSQL DB
    Medicine INT NOT NULL,
    Dosage VARCHAR (20) NOT NULL, -- Dosage Format : <Morning>-<Afternoon>-<Night>
    Duration INT NOT NULL, -- Duration of Medicine in Days
    dt DATE NOT NULL,

    PRIMARY KEY (ID, Patient, Medicine),
    FOREIGN KEY (Patient) REFERENCES Patient (ID),
    FOREIGN KEY (Medicine) REFERENCES Medicine (ID)
);

