import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
from model.Vaccine import Vaccine

class Patient:
    def __init__(self, username, password=None, salt=None, hash=None):
        self.username = username
        self.password = password
        self.salt = salt
        self.hash = hash

    # getters
    def get(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        get_patient_details = "SELECT Salt, Hash FROM Patients WHERE " \
                             "Username = %s"
        try:
            cursor.execute(get_patient_details, self.username)
            for row in cursor:
                curr_salt = row['Salt']
                curr_hash = row['Hash']
                calculated_hash = Util.generate_hash(self.password, curr_salt)
                if not curr_hash == calculated_hash:
                    print("Incorrect password")
                    cm.close_connection()
                    return None
                else:
                    self.salt = curr_salt
                    self.hash = calculated_hash
                    cm.close_connection()
                    return self
        except pymssql.Error as e:
            print("Error occurred when fetching current patient")
            raise e
        finally:
            cm.close_connection()
        return None

    def get_username(self):
        return self.username

    def get_salt(self):
        return self.salt

    def get_hash(self):
        return self.hash

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_patients = "INSERT INTO Patients VALUES (%s, %s, %s)"
        try:
            cursor.execute(add_patients, (self.username, self.salt, self.hash))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()

    def make_reservation(self, appointment_ID, date, vax_info,
                             available_caregivers):

        # First adjust vaccine availability in vaccine table
        vaccine_name = vax_info[0]
        doses = vax_info[1]
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

        try:
            vaccine.decrease_available_doses(1)
        except pymssql.Error as e:
            print("Failed to increase available doses for Vaccine")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Failed to increase available doses for Vaccine")
            print("Error:", e)
            return

        # next remove availability of this caregiver on this day
        assigned_caregiver = available_caregivers[0]
        Util.remove_availability(date, assigned_caregiver)

        #finally schedule appointment
        Util.schedule_appointment(appointment_ID, date, assigned_caregiver,
                                  self.username,
                                  vaccine_name)
        print (f"Appointment {appointment_ID} scheduled for {self.username} on"
               f" {date} with "
               f"{assigned_caregiver} to recieve the {vaccine_name} vaccine.")

    def get_appointments(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        get_appointments = "SELECT * FROM Appointments WHERE Patient = %s"

        try:
            cursor.execute(get_appointments, (self.username))
            #For patients, you should print the appointment ID, vaccine name, date, and caregiver name.
            appointments = []
            for row in cursor:
                appointment_ID = row[0]
                date = row[1]
                caregiver = row[2]
                vaccine = row[4]
                appointments.append((appointment_ID, date, caregiver, vaccine))
            return appointments
        except pymssql.Error:
            print("Error occurred when updating Appointments")
            raise
        finally:
            cm.close_connection()