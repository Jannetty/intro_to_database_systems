CREATE TABLE InsuranceCo(
  name VARCHAR(100) PRIMARY KEY,
  phone INT
);

CREATE TABLE Person(
  ssn INT PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE Driver(
  ssn INT PRIMARY KEY REFERENCES Person(ssn),
  driverID INT
);

CREATE TABLE NonProfessionalDriver(
  ssn INT PRIMARY KEY REFERENCES Driver(ssn)
);

CREATE TABLE ProfessionalDriver(
  ssn INT PRIMARY KEY REFERENCES Driver(ssn),
  medicalHistory VARCHAR(100)
);

CREATE TABLE Vehicle(
  licensePlate VARCHAR(10) PRIMARY KEY,
  year INT,
  insured_by VARCHAR(100) REFERENCES InsuranceCo(name),
  maxLiability REAL,
  owner INT REFERENCES Person(ssn)
);

CREATE TABLE Car(
  licensePlate VARCHAR(10) PRIMARY KEY REFERENCES Vehicle(licensePlate),
  make VARCHAR(100)
);

CREATE TABLE Drives(
  driver_ssn INT REFERENCES nonProfessionalDriver(ssn),
  car_licensePlate VARCHAR(10) REFERENCES Car(licensePlate),
  PRIMARY KEY(driver_ssn, car_licensePlate)
);

CREATE TABLE Truck(
  licensePlate VARCHAR(10) PRIMARY KEY REFERENCES Vehicle(licensePlate),
  capacity INT,
  operated_by INT REFERENCES ProfessionalDriver(ssn)
);

/*
Comment 1: The relation in my relational schema that represents the relationship
"insures" is the insured_by field in the Vehicle table. This is my representation
because each vehicle is insured by at most 1 insurance company, so I can store
that insurance company (or Null if a vehicle is uninsured) in a field in the
Vehicle table (that references the insurance company in the InsuranceCo table)
without needing to make an additional table.



Comment 2: The drives relationship is represented with a table and the operates
relationship is represented with a field in the Trucks table. These relationships
are represented differently because the drives relationship is many-to-many
and the operates relationship is many-to-one.

The drives relationship is represented in my schema as a table. This is
because the relationship between cars and nonProfessionalDrivers is many to many,
so any number of drivers could drive a car and a driver can drive any number of
cars. In order to capture this, I need a table that stores every driver-car
relationship. I name this table "Drives".

The operates relationship is represented in my schema as the "operated_by" field
in the Truck table. This is because each truck is driven by at most one
ProfessionalDriver. This means, like in the insures relationship above, I can
store the operator of each truck (if a truck has an operator, otherwise store
Null) in that Truck's tuple in the Truck's table. That operated_by field is a
foreign key to the ProfessionalDriver table so additional information can be
found about each driver.

*/
