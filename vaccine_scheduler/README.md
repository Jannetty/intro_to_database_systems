# Python Application for Vaccine Scheduler

A common type of application that connects to a database is a reservation system, where users schedule time slots for some centralized resource. In this project I programmed part of an appointment scheduler for vaccinations, where the users are patients and caregivers keeping track of vaccine stock and appointments. This application ran on the command line terminal, and connected to a database server I created with my [Microsoft Azure](https://azure.microsoft.com/en-us/) account. This server is no longer running and thus the code will no longer run.

### Overview of functionality

This vaccine scheduler allows patients and caregivers to create usernames. Usernames must be unique within their class (i.e. no two patients can have the same username, but a patient and a caregiver can have the same username). Account passwords are salted and hashed. Once an account is created, patients and caregivers can login. Once logged in, caregivers can update vaccine quantities and update their availabilities. Patients can search to see all available caregivers and vaccines on a given date and can reserve appointments to recieve a specific vaccine on a specific day. Caregivers are assumed to only be able to have one vaccine appointment per day. Logged in patients can cancel their own appointments and logged in caregivers can cancel any appointments.

### Part 1: Completed design of database schema with entity relationship diagram and create table statements.
Entity Relationship diagram for database in src/main/resources/design.pdf. Create tables statements found in src/main/resources/create.sql.

### Part 2: Code Implementation

For this project I worked in a pyenv virtual environment. To interact with the SQL Server, I had to add the following lines to the `activate` file in my virtual environment's `bin` directory. 
```bash
## Environment variables for this project
export Server=name_of_my_server.database.windows.net
export DBName=name_of_my_database
export UserID=my_username@name_of_my_server.database.windows.net
export Password=my_password
```
and within the `deactivate` function:
```bash
unset Server
unset DBName
unset UserID
unset Password
```
To make this code run again, one would need to have a new SQL server and set the environment variables of their python environment as was done in these statements above.

The rest of my implementation was extended from code provided by the [CSE414](https://sites.google.com/cs.washington.edu/cse414-22wi/home) teaching staff.

I implemented the [patient class](src/main/scheduler/model/Patient.py) based on the provided [caregiver class](src/main/scheduler/model/Caregiver.py).

Functions I implemented are as follows:

***create_patient*** (in [Scheduler.py](src/scheduler/Scheduler.py)) adds a new patient to the Patients table if new patient's 
username is not in the Patients already. Duplicate usernames are not permitted.

***create_caregiver*** (in [Scheduler.py](src/scheduler/Scheduler.py)) adds a new caregiver to the Caregivers table if new caregiver's username is not in Caregivers already. Duplicate usernames are not permitted.

***login_patient*** (in [Scheduler.py](src/scheduler/Scheduler.py)) logs patient in if the patient username exists in the Patients 
table and the username's correct password is entered.

***login_caregiver*** (in [Scheduler.py](src/scheduler/Scheduler.py)) logs caregiver in if the caregiver username exists in the Caregivers table and the username's correct password is entered.

***search_caregiver_schedule*** (in [Scheduler.py](src/scheduler/Scheduler.py)) returns all available caregivers and vaccines (with doses) available on a given date. Patients and Caregivers can search_caregiver_schedule if they are logged in.

***reserve*** (in [Scheduler.py](src/scheduler/Scheduler.py)) allows a patient to reserve a vaccination appointment to recieve a 
specified vaccine on a specified date. A random available caregiver is 
assigned to the appointment. This decreases the available doses 
for the vaccine by one in the Vaccines table, removes the availability for 
the assigned caregiver from the Availabilities table, and creates a new 
entry in the Appointments table. Only logged in patients can reserve 
appointments.

***upload_availability*** (in [Scheduler.py](src/scheduler/Scheduler.py)) allows caregivers to upload their availability. 
Caregivers cannot upload availability for a day when they have a scheduled appointment (**caregivers can only administer one vaccine per day**). They can also not upload multiple availabilities for the same day. This function adds a new entry to the Availabilities table.

***cancel*** (in [Scheduler.py](src/scheduler/Scheduler.py)) cancels an appointment by deleting it from the Appointments table adding the caregiver's availability back to the Availability table, and adding a dose of the vaccine back to the Vaccines table. Logged in caregivers can cancel any appointment. Logged in patients can only cancel 
their own appointments. Unlogged in users cannot use this function.

***add_doses*** (in [Scheduler.py](src/scheduler/Scheduler.py)) allows logged in caregivers to add doses of a vaccine to the 
Vaccines table.

***show_appointments*** (in [Scheduler.py](src/scheduler/Scheduler.py)) shows a logged-in user all appointments that user has in 
the Appointments table.

***logout*** (in [Scheduler.py](src/scheduler/Scheduler.py)) logs a user out.
