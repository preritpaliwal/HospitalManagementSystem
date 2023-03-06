INSERT INTO Login_Table VALUES (1, 'Front Desk Operator', 'Vibhu');
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