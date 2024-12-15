---------------------------DB AND SERVER INFORMATION--------------------------- 
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;

--------------------------- TABLE CREATION--------------------------- 
--(50) is the max num of characters that username can contain this is an arbitrary number 
CREATE TABLE students (
    name VARCHAR(50) NOT NULL, -- name of the student 
    uid VARCHAR(20) NOT NULL -- this is going to be the uid, each student has an associated uid
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE tasks (
    date DATE NOT NULL, -- deadline
    subject VARCHAR(50) NOT NULL, -- the length of the string are not going to be less than 50 to be safe
    name VARCHAR(50) NOT NULL -- name of the work
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE timetable (
    day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL, 
    hour TIME NOT NULL,
    subject VARCHAR(50) NOT NULL,
    class VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;    

CREATE TABLE marks (
    uid VARCHAR(10) NOT NULL,
    subject VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL, -- name of the exam or task
    mark DECIMAL(4,2) NOT NULL -- 4 digits in total, 2 reserved for decimals
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--------------------------- INSERT INFORMATION--------------------------- 

INSERT INTO students (name, uid) VALUES
('Ivan Rodriguez', '4BD56667'), 
('Junle Wang', '5F63B81E'),
('Blanca Calero', 'B3C4BA24'),
('Mariona Capdevila', '72B6E200'),
('Roger Garcia', '24BAC4B3');

INSERT INTO tasks (date, subject, name) VALUES
('2024-11-25', 'DSBM', 'Practica 5'),
('2024-10-21', 'DSBM', 'Practica 2'),
('2024-09-27', 'RP', 'Control 1'),
('2024-10-13', 'RP', 'Control 2'),
('2024-11-17', 'RP', 'Control 3'),
('2024-12-30', 'PSAVC', 'Practica 1'),
('2024-12-11', 'PSAVC', 'Pràctica 2'),
('2024-12-27', 'PBE', 'CDR'),
('2024-11-13', 'PBE', 'Entrega PUZZLE2');

INSERT INTO timetables (day, hour, subject, class)VALUES 
('Monday', '08:00:00', 'RP_LAB', 'Aula D3006'), 
('Monday', '10:00:00', 'RP_TEORIA', 'Aula A4105'), 
('Monday', '11:00:00', 'DSBM_TEORIA', 'Aula A4105'),
('Tuesday', '08:00:00', 'PSAVC_TEORIA', 'Aula A4105'),  
('Tuesday', '11:00:00', 'TD_TEORIA', 'Aula A4105'),
('Wednesday', '08:00:00', 'PBE_LAB', 'Aula A4105'),
('Thursday', '08:00:00', 'PBE_TEORIA', 'Aula A4105'),
('Thursday', '10:00:00', 'RP_TEORIA', 'Aula A4105'),
('Thursday', '12:00:00', 'DSBM_LAB', 'Aula C5S101A'),
('Friday', '08:00:00', 'DSBM_TEORIA', 'Aula A4105'),
('Friday', '10:00:00', 'PSAVC', 'Aula A4105'),
('Friday', '12:00:00', 'TD', 'Aula A4105');

INSERT INTO marks (uid, subject, name, mark)VALUES
('4BD56667', 'DSBM', 'Examen Parcial', 3.75), 
('4BD56667', 'RP', 'Examen Parcial', 2),
('4BD56667', 'PSAVC', 'Examen Parcial', 2),
('4BD56667', 'TD', 'Examen Parcial', 3),
('4BD56667', 'PBE', 'Examen Parcial', 8),
('5F63B81E', 'DSBM', 'Examen Parcial', 6),
('5F63B81E', 'RP', 'Examen Parcial', 0.7),
('5F63B81E', 'PSAVC', 'Examen Parcial', 2.8),
('5F63B81E', 'TD', 'Examen Parcial', 4.75),
('5F63B81E', 'PBE', 'Examen Parcial', 8.7),
('B3C4BA24', 'DSBM', 'Examen Parcial', 5.7),
('B3C4BA24', 'RP', 'Examen Parcial', 1.2),
('B3C4BA24', 'PSAVC', 'Examen Parcial', 6.6),
('B3C4BA24', 'TD', 'Examen Parcial', 3.4),
('B3C4BA24', 'PBE', 'Examen Parcial', 7.2),
('72B6E200', 'DSBM', 'Examen Parcial', 2.5),
('72B6E200', 'RP', 'Examen Parcial', 3.75),
('72B6E200', 'PSAVC', 'Examen Parcial', 8.5),
('72B6E200', 'TD', 'Examen Parcial', 4),
('72B6E200', 'PBE', 'Examen Parcial', 5.6),
('24BAC4B3', 'DSBM', 'Examen Parcial', 7),
('24BAC4B3', 'RP', 'Examen Parcial', 3),
('24BAC4B3', 'PSAVC', 'Examen Parcial', 4.5),
('24BAC4B3', 'TD', 'Examen Parcial', 2),
('24BAC4B3', 'PBE', 'Examen Parcial', 6);


