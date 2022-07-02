CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Patients(
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Appointments(
    AppointmentID varchar(32),
    Time date,
    Caregiver varchar(255) REFERENCES Caregivers(Username),
    Patient varchar(255) REFERENCES Patients(Username),
    Vaccine varchar(255) REFERENCES Vaccines(Name),
    PRIMARY KEY (AppointmentID)
);