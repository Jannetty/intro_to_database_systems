import hashlib
import os
import sys
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymssql

class Util:
    def generate_salt():
        return os.urandom(16)

    def generate_hash(password, salt):
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,
            dklen=16
        )
        return key

    def get_available_caregivers(search_date):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        get_caregivers = "SELECT Username FROM Availabilities WHERE " \
                         "Time = %s"
        available_caregivers = []
        try:
            cursor.execute(get_caregivers, search_date)
            for row in cursor:
                curr_username = row[0]
                available_caregivers.append(curr_username)
        except pymssql.Error:
            print("Error connecting to server, failed search")
            raise
        finally:
            cm.close_connection()
            return available_caregivers

    def get_available_vaccines():
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        get_vaccines = "SELECT * FROM Vaccines WHERE " \
                         "Doses > 0"
        available_vaccines = []
        try:
            cursor.execute(get_vaccines)
            for row in cursor:
                curr_vax = row[0]
                curr_doses = row[1]
                available_vaccines.append((curr_vax, curr_doses))
        except pymssql.Error:
            print("Error connecting to server, failed search")
            raise
        finally:
            cm.close_connection()
            return available_vaccines

    def remove_availability(date, caregiver):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        delete_availability = "DELETE FROM Availabilities WHERE " \
                         "Time = %s AND Username = %s"
        try:
            cursor.execute(delete_availability, (date, caregiver))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            print("Error connecting to server, failed to update availability")
            raise
        finally:
            cm.close_connection()

    def schedule_appointment(appointment_ID, date, caregiver, patient, vaccine):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_availability = "INSERT INTO Appointments VALUES (%s, %s , %s, %s, %s)"

        try:
            cursor.execute(add_availability,(appointment_ID, date, caregiver,
                                             patient, vaccine))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.Error:
            print("Error occurred when updating caregiver availability")
            raise
        finally:
            cm.close_connection()

    def get_appointment(appointment_id):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        get_appointment = "SELECT * FROM Appointments WHERE AppointmentID = %s"

        try:
            cursor.execute(get_appointment, (appointment_id))
            if cursor.rowcount == 0:
                print(f"{appointment_id} is invalid Appointment ID.")
                return None
            for row in cursor:
                appointment_info = row
            return appointment_info
        except pymssql.Error:
            print("Error occured when searching for appointment")
            raise
        finally:
            cm.close_connection()