INSERT INTO Login_Table VALUES (1, 'Front Desk Operator', 'Vibhu');
INSERT INTO Login_Table VALUES (2, 'Data Entry Operator','Prerit');
INSERT INTO Login_Table VALUES (3, 'Doctor', 'Deepsikha');
INSERT INTO Login_Table VALUES (4, 'Doctor', 'Anushka');
INSERT INTO Login_Table VALUES (5, 'Database Administrator', 'Umika');

INSERT INTO Doctor VALUES (3, 'Deepsikha', 'Physician', 'deepsikhabehera2811@gmail.com', '1234567890');
INSERT INTO Doctor VALUES (4, 'Anushka', 'Cardiology', 'anushkas12345@gmail.com', '1234554321');

INSERT INTO Room VALUES ('A-101', 1, 1);
INSERT INTO Room VALUES ('A-102', 1, 1);
INSERT INTO Room VALUES ('A-103', 3, 3);
INSERT INTO Room VALUES ('A-104', 3, 3);
INSERT INTO Room VALUES ('A-105', 3, 3);
INSERT INTO Room VALUES ('A-106', 2, 2);
INSERT INTO Room VALUES ('A-107', 2, 2);

INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Vibhu', '1111111111', 'vibhuyadav41002@gmail.com', 'Addressssssss', '12345');
INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Prerit', '1111111112', 'prerit@gmail.com', 'Addressssssss', '12346');
INSERT INTO Patient(Name, Phone, Email, Address, InsuranceID) VALUES ( 'Umika', '1111111113', 'umika@gmail.com', 'Addressssssss', '12347');

INSERT INTO Test_Treatment VALUES ("BT101", "Blood Test", 300, "Test");
INSERT INTO Test_Treatment VALUES ("EC101", "ECG", 5000, "Test");
INSERT INTO Test_Treatment VALUES ("MR101", "MRI", 7000, "Test");
INSERT INTO Test_Treatment VALUES ("Preg101", "Ultrasound", 2000, "Test");
INSERT INTO Test_Treatment VALUES ("Cancer601", "Chemo", 10000000, "Treatment");
INSERT INTO Test_Treatment VALUES ("Preg601", "Delivery", 200000, "Treatment");
INSERT INTO Test_Treatment VALUES ("Kidney601", "Dialysis", 6000, "Treatment");

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
INSERT INTO Medicine (Name, Manufacturer, Price) VALUES ('Combiflam', 'Apollo', 30);
INSERT INTO Medicine (Name, Manufacturer, Price) VALUES ('Morphine', 'Sun Pharma', 70);

INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (1, 3, '1-1-0' , 5 , '2023-03-04');
INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (2, 1, '1-0-0' , 5 , '2023-03-04');
INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (2, 2, '1-0-0' , 5 , '2023-03-04');
INSERT INTO Prescribes (Patient, Medicine, Dosage, Duration, dt) VALUES (3, 1, '1-0-0' , 5 , '2023-03-04'); 