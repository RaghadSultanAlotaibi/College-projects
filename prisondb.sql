-- CREATE DATABASE prisondb;
USE prisondb;
CREATE TABLE Prison (
    Section_id INT PRIMARY KEY,
    Section_name VARCHAR(100),
    No_of_prisoners INT
);
CREATE TABLE Crime (
    Crime_id INT PRIMARY KEY,
    Crime_name VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT,
    Penalty VARCHAR(100)
);
-- cascade
CREATE TABLE Prisoners (
    Prisoner_id INT PRIMARY KEY,
    Section_id INT,
    Date_of_arrest DATE,
    Address VARCHAR(255),
    Nationality VARCHAR(100),
    Section_duration INT,
    Crime_id int,
    Prisoners_states VARCHAR(50),
    name varchar(100),
    age int,
    gender varchar(10),
    FOREIGN KEY (Section_id) REFERENCES Prison(Section_id),
    FOREIGN KEY (Crime_id) REFERENCES Crime(Crime_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE Employee (
    Employee_id INT PRIMARY KEY,
    Section_id INT,
    Job_title VARCHAR(100),
    Nationality VARCHAR(100),
    Salary DECIMAL(10,2),
    Phone_number VARCHAR(15),
    Date_of_employment DATE,
    name varchar(100),
    age int,
    password_hash CHAR(64),
    FOREIGN KEY (Section_id) REFERENCES Prison(Section_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE Visitors (
    Visitor_id INT PRIMARY KEY,
    Section_id INT,
    Visit_date DATE,
    Visit_nature VARCHAR(100),
    name varchar(100),
    age int,
    FOREIGN KEY (Section_id) REFERENCES Prison(Section_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


INSERT INTO Prison (Section_id, Section_name, No_of_prisoners) VALUES
(1, 'Central Prison', 2),
(2, 'North Correctional Facility', 1),
(3, 'East Block Facility', 4),
(4, ' Southern Correctional Center', 2);

INSERT INTO Crime (Crime_id, Crime_name, Description, Penalty) VALUES
(1, 'Assault', 'Unlawful physical attack or threat on another person.', 'Up to 7 years imprisonment'),
(2, 'Fraud', 'Wrongful deception intended to result in financial or personal gain.', 'Up to 5 years imprisonment'),
(3, 'Robbery', 'Taking property unlawfully from a person by force or threat.', 'Up to 10 years imprisonment'),
(4, 'Drug Trafficking', 'Illegal trade and distribution of controlled substances.', 'Up to 15 years imprisonment'),
(5, 'Murder', 'The unlawful killing of another human being with intent.', 'Life imprisonment or death penalty'),
(6, 'Cybercrime', 'Criminal activities carried out using computers or the internet.', 'Up to 8 years imprisonment'),
(7, 'Forgery', 'The act of falsely making or altering a document with intent to defraud.', 'Up to 6 years imprisonment');
INSERT INTO Prisoners (Prisoner_id, Section_id, Date_of_arrest, Address, Nationality, Section_duration, Crime_id, Prisoners_states, name, age, gender)
VALUES
(2, 1, '2019-08-21', '456 Oak Rd', 'Egypt', 7, 1, 'Active', 'Ali', 34, 'Male'),
(3, 2, '2021-03-15', '789 Pine Ave', 'UK', 3, 2, 'Inactive', 'Emily Clark', 29, 'Female'),
(4, 3, '2022-07-14', '202 Elm St', 'Germany', 8, 3, 'Active', 'Lukas Schmidt', 31, 'Male'),
(5, 3, '2021-12-02', '89 Stone Ave', 'Mexico', 6, 4, 'Active', 'Carlos Mendez', 34, 'Male'),
(6, 3, '2020-03-28', '142 Cedar Dr', 'USA', 10, 5, 'Solitary', 'Michael Brown', 45, 'Male'),
(7, 3, '2023-01-19', '33 River Rd', 'France', 3, 2, 'Active', 'Jean Dupont', 28, 'Male'),
(8, 4, '2022-09-11', '56 Hilltop Blvd', 'India', 2, 6, 'Inactive', 'Priya Verma', 26, 'Female'),
(9, 4, '2023-06-07', '908 Forest Lane', 'Brazil', 1, 7, 'Active', 'Ana Souza', 30, 'Female');

INSERT INTO Employee (Employee_id, Section_id, Job_title, Nationality, Salary, Phone_number, Date_of_employment, name, age, password_hash)
VALUES
(1, 1, 'Warden', 'USA', 5000.00, '123-456-7890', '2015-06-01', 'Sarah Blake', 45, SHA2('warden123', 256)),
(2, 1, 'Guard', 'Canada', 3500.00, '234-567-8901', '2018-09-15', 'Tom Richards', 39, SHA2('guard456', 256)),
(3, 2, 'Medical Officer', 'Jordan', 4000.00, '345-678-9012', '2020-01-10', 'Layla Haddad', 36, SHA2('medic789', 256)),
(4, 3, 'Security Supervisor', 'USA', 4800.00, '555-789-3456', '2017-04-10', 'John Carter', 42, SHA2('secure321', 256)),
(5, 3, 'Maintenance Head', 'Philippines', 3000.00, '555-654-8765', '2019-11-23', 'Marites Dela Cruz', 40, SHA2('maint456', 256)),
(6, 4, 'Counselor', 'UK', 4200.00, '555-111-2222', '2021-05-14', 'Harry Green', 38, SHA2('counsel999', 256)),
(7, 4, 'Nurse', 'Italy', 3900.00, '555-222-3333', '2022-07-01', 'Giulia Romano', 33, SHA2('nurse1010', 256));

INSERT INTO Visitors (Visitor_id, Section_id, Visit_date, Visit_nature, Name, Age) VALUES
(1, 1, '2025-04-10', 'Family', 'Maria Lopez', 32),
(2, 2, '2025-04-12', 'Legal', 'James Wu', 29),
(3, 1, '2025-04-11', 'Friend', 'Emma Johnson', 27),
(4, 3, '2025-04-10', 'Legal', 'Omar Ali', 35),
(5, 3, '2025-04-11', 'Family', 'Sophia Kim', 31),
(6, 4, '2025-04-13', 'Friend', 'Daniel Murphy', 37),
(7, 4, '2025-04-14', 'Religious', 'Fatima Hassan', 34);



-- view
CREATE  VIEW ActivePrisoners AS
SELECT 
    p.Prisoner_id,
    c.Crime_name AS Crime,
    p.Prisoners_states,
    pr.Section_name
FROM Prisoners p
JOIN Prison pr ON p.Section_id = pr.Section_id
JOIN Crime c ON p.Crime_id = c.Crime_id
WHERE p.Prisoners_states = 'Active';

-- view example
SELECT * FROM ActivePrisoners;
-- See view definition
 SHOW CREATE VIEW ActivePrisoners;
-- List all views in the database
 SHOW FULL TABLES IN prisondb WHERE TABLE_TYPE = 'VIEW';

 -- trigger
 DELIMITER $$
CREATE TRIGGER CheckDurationBeforeInsert
BEFORE INSERT ON Prisoners
FOR EACH ROW
BEGIN
    IF NEW.Section_duration > 50 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Section duration cannot exceed 50 years.';
    END IF;
END $$
DELIMITER ;


-- trigger example 

 INSERT INTO Prisoners (
   Prisoner_id, Section_id, Date_of_arrest, Address, Nationality,
   Section_duration, Crime_id, Prisoners_states, name, age, gender
) VALUES (
    10, 1, '2025-01-01', '100 Jail St', 'USA',
    60, '1', 'Active', 'Jake Flame', 35, 'Male'
 );

 -- See Trigger List
SHOW TRIGGERS;

-- index 
-- Index on Prisoners for foreign key and state filter
CREATE INDEX idx_prisoners_section_id ON Prisoners(Section_id);
CREATE INDEX idx_prisoners_state ON Prisoners(Prisoners_states);
-- Index on Employees and Visitors section for faster joins
CREATE INDEX idx_employees_section_id ON Employee(Section_id);
CREATE INDEX idx_visitors_section_id ON Visitors(Section_id);

-- index example
 SHOW INDEX FROM Prisoners;
 SHOW INDEX FROM Employee;
 SHOW INDEX FROM Visitors;

-- hash example
 SELECT Employee_id, name, password_hash FROM Employee;

-- cascade example
-- delete cascade
 DELETE FROM Prison WHERE Section_id = 1;
-- update cascade
 UPDATE Prison
 SET Section_id = 99
 WHERE Section_id = 2 ;

 SELECT * FROM Prison WHERE Section_id = 99;
 SELECT * FROM Prisoners WHERE Section_id = 99;
 SELECT * FROM Employee WHERE Section_id = 99;
 SELECT * FROM Visitors WHERE Section_id = 99;

-- Change Crime_id 1 to 101
 UPDATE Crime SET Crime_id = 101 WHERE Crime_id = 1;

-- Then check Prisoners table
 SELECT Prisoner_id, Crime_id FROM Prisoners WHERE Crime_id = 101;


select * from prisoners;
select * from crime;





