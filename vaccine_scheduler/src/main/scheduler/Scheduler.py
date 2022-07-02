from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from uuid import uuid4
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    """
    TODO: Part 1 (done)
    """
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again using the format: create_patient <username> "
              "<password>")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Create patient failed, Cannot save")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
        return
    print(" *** Account created successfully *** ")

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again using the format: create_caregiver <username> "
              "<password>")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Create caregiver failed, Cannot save")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
        return
    print(" *** Account created successfully *** ")


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    """
    TODO: Part 1 (done)
    """
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_patient is not None or current_caregiver is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again using the format login_patient <username> "
              "<password>")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login patient failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Patient logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again using the format login_caregiver <username> "
              "<password>")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login caregiver failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when logging in. Please try again!")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Error occurred when logging in. Please try again!")
    else:
        print("Caregiver logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2 (done)
    """
    # Output all caregivers available at certain date
    # Output all vaccines with doses left
    if len(tokens) != 2:
        print("Please search caregiver schedule with the following format: "
              "search_caregiver_schedule <date>")
        return
    if current_caregiver is None and current_patient is None:
        print("Please login before searching!")
        return
    search_date = tokens[1]

    available_caregivers = Util.get_available_caregivers(search_date)
    available_vaccines = Util.get_available_vaccines()
    print(f"Caregivers available on {search_date}:")
    for caregiver in available_caregivers:
        print(caregiver)
    if available_caregivers == []:
        print(f"No caregivers available on {search_date}")
    print("Available vaccines:")
    for vax_doses in available_vaccines:
        print(f"{vax_doses[0]}, {vax_doses[1]} dose(s) available")

def reserve(tokens):
    """
    TODO: Part 2 (done)
    """
    if len(tokens) != 3:
        print("Please reserve using the following format: reserve <date> "
              "<vaccine>")
        return

    if current_patient is None:
        print("Only logged-in patients can reserve appointments.")
        return

    date = tokens[1]
    vaccine = tokens[2]

    if appointment_exists_patient_date(current_patient.username, date):
        print(f"Patient {current_patient.username} already has an appointment "
              f"on {date}. We are limiting appointments to one per patient "
              f"per day at this time.")
        return

    available_caregivers = Util.get_available_caregivers(date)
    if len(available_caregivers) == 0:
        print(f"No appointments available on {date}. Please choose an "
              f"appointment date with available caregivers.")
        return
    available_vaccines = Util.get_available_vaccines()
    vax_info = [vax_dose for vax_dose in available_vaccines if vax_dose[0] ==
                vaccine]
    if vax_info == []:
        print(f"No {vaccine} doses available. Please choose a vaccine with "
              f"available doses.")
        return
    # We now know there is a caregiver and a vaccine available for this patient
    current_patient.make_reservation(uuid4().hex, date, vax_info[0],
                             available_caregivers)

def appointment_exists_patient_date(patient, date):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_patient_date = "SELECT * FROM Appointments WHERE Patient = %s AND " \
                          "Time = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_patient_date, (patient, date))
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Patient'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    try:
        date_tokens = date.split("-")
        month = int(date_tokens[0])
        day = int(date_tokens[1])
        year = int(date_tokens[2])
    except:
        print("Please input dates in format mm-dd-yyyy")
        return
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return


def cancel(tokens):
    """
    TODO: Extra Credit (done)
    """
    # get appointment information
    # delete the appointment
    if len(tokens) != 2:
        print("Please use the format cancel <appointment_id")
        return

    if current_caregiver is None and current_patient is None:
        print("No user logged in. Please login to cancel appointments")
        return

    appointment_ID = tokens[1]
    appointment_info = Util.get_appointment(appointment_ID)
    if appointment_info == None:
        print("No appointment cancelled.")
        return

    if current_caregiver is None:
        if appointment_info[3] != current_patient.username:
            print(f"Current Patient is not in appointment {appointment_ID}. "
                    "Patients can only cancel their own appointments. No "
                    "Appointment cancelled.")

    # increase available vaccine doses
    vaccine = Vaccine(appointment_info[4], None).get()
    vaccine.increase_available_doses(1)

    # add availability back for the Caregiver
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()
    add_availability = "INSERT INTO Availabilities VALUES (%s , %s)"
    try:
        cursor.execute(add_availability, (appointment_info[1],
                                            appointment_info[2]))
        # you must call commit() to persist your data if you don't set autocommit to True
        conn.commit()
    except pymssql.Error:
        print("Error occurred when updating caregiver availability")
        raise
    finally:
        cm.close_connection()

    # delete appointment
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor()
    delete_appointment = "DELETE FROM Appointments WHERE AppointmentID = %s"
    try:
        cursor.execute(delete_appointment, (appointment_info[0]))
        # you must call commit() to persist your data if you don't set autocommit to True
        conn.commit()
    except pymssql.Error:
        print("Error occurred when deleting appointment")
        raise
    finally:
        cm.close_connection()

    print(f"Appointment {appointment_ID} canceled")

def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Failed to get Vaccine information")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to get Vaccine information")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Failed to add new Vaccine to database")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to add new Vaccine to database")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Failed to increase available doses for Vaccine")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to increase available doses for Vaccine")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2 (done)
    '''
    if current_caregiver is None:
        if current_patient is None:
            print("No user logged in. Cannot show appointments.")
            return
        print(f"Appointments for {current_patient.username}:")
        user_appointments = current_patient.get_appointments()
        for appointment in user_appointments:
            print(f"Appointment ID: "
                  f"{appointment[0]} | Date: {appointment[1]} | "
                  f"Caregiver: {appointment[2]} | Vaccine: {appointment[3]}")
    else:
        if current_caregiver is None:
            print("No user logged in. Cannot show appointments.")
            return
        print(f"Appointments for {current_caregiver.username}:")
        user_appointments = current_caregiver.get_appointments()
        for appointment in user_appointments:
            print(f"Appointment ID: "
                  f"{appointment[0]} | Date: {appointment[1]} | "
                  f"Patient: {appointment[2]} | Vaccine: {appointment[3]}")


def logout(tokens):
    """
    TODO: Part 2 (done)
    """
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("No user is currently logged in. No logout performed.")
        return
    if current_caregiver is not None:
        username = current_caregiver.username
        current_caregiver = None
        print(f"Logged out {username}")
    elif current_patient is not None:
        username = current_patient.username
        current_patient = None
        print(f"Logged out {username}")
    return


def start():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
        print("> create_caregiver <username> <password>")
        print("> login_patient <username> <password>")  #// TODO: implement login_patient (Part 1)
        print("> login_caregiver <username> <password>")
        print("> search_caregiver_schedule <date>")  #// TODO: implement search_caregiver_schedule (Part 2)
        print("> reserve <date> <vaccine>") #// TODO: implement reserve (Part 2)
        print("> upload_availability <date>")
        print("> cancel <appointment_id>") #// TODO: implement cancel (extra credit)
        print("> add_doses <vaccine> <number>")
        print("> show_appointments")  #// TODO: implement show_appointments (Part 2)
        print("> logout") #// TODO: implement logout (Part 2)
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Try Again")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
