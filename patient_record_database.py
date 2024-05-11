#Category 2 Database and Backend Development
#Task 1: Build a Patient Record Management System

# Importing necessary modules for building the graphical user interface and managing data
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

# Importing SQLite for database management
import sqlite3

# Creating the graphical user interface for the Patient Record Management System
class PatientRecordSystemGUI:
    # Initializing the main window
    def __init__(self, master):
        self.master = master
        self.master.title("Patient Record Management System")

        # Initializing the PatientRecordSystem to manage patient records
        self.patient_system = PatientRecordSystem()

        # Creating and configuring UI components
        self.label_name = tk.Label(master, text="Patient Name:")
        self.entry_name = tk.Entry(master)

        self.label_dob = tk.Label(master, text="Date of Birth (YYYY-MM-DD):")
        self.entry_dob = tk.Entry(master)

        self.label_diagnosis = tk.Label(master, text="Diagnosis:")
        self.entry_diagnosis = tk.Entry(master)

        self.button_add = tk.Button(master, text="Add Patient", command=self.add_patient)
        self.button_update = tk.Button(master, text="Update Diagnosis", command=self.open_update_diagnosis_window)
        self.button_fetch = tk.Button(master, text="Fetch Records", command=self.fetch_records)

        # Adding Listbox to select a patient
        self.label_patient_list = tk.Label(master, text="Select Patient:")
        self.patient_listbox = tk.Listbox(master)
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_select)

        # Creating a grid layout for UI components
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_dob.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_dob.grid(row=1, column=1, padx=10, pady=5)

        self.label_diagnosis.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_diagnosis.grid(row=2, column=1, padx=10, pady=5)

        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_update.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_fetch.grid(row=5, column=0, columnspan=2, pady=10)

        # Adding Listbox components to the grid
        self.label_patient_list.grid(row=6, column=0, columnspan=2, pady=5)
        self.patient_listbox.grid(row=7, column=0, columnspan=2, pady=5)

        # Initializing patient listbox
        self.update_patient_list()

    # Method to add a new patient
    def add_patient(self):
        name = self.entry_name.get()
        dob = self.entry_dob.get()
        diagnosis = self.entry_diagnosis.get()

        if name and dob:
            try:
                aadhar_no = simpledialog.askstring("Input", "Enter Aadhar Number:")
                self.patient_system.add_patient(aadhar_no, name, dob, diagnosis)
                messagebox.showinfo("Success", "Patient added successfully!")
                self.update_patient_list()  # Updating patient list after adding a new patient
            except Exception as e:
                messagebox.showerror("Error", f"Error adding patient: {str(e)}")
        else:
            messagebox.showerror("Error", "Name and Date of Birth are required fields.")

    # Method to open a window for updating patient diagnosis
    def open_update_diagnosis_window(self):
        aadhar_no = simpledialog.askstring("Input", "Enter Aadhar Number:")
        if aadhar_no:
            update_diagnosis_window = tk.Toplevel(self.master)
            update_diagnosis_window.title("Update Diagnosis")

            label_diagnosis = tk.Label(update_diagnosis_window, text="Diagnosis:")
            entry_diagnosis = tk.Entry(update_diagnosis_window)

            button_update_diagnosis = tk.Button(update_diagnosis_window, text="Update Diagnosis",
                                                command=lambda: self.update_diagnosis(aadhar_no, entry_diagnosis.get(), update_diagnosis_window))

            label_diagnosis.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
            entry_diagnosis.grid(row=0, column=1, padx=10, pady=5)
            button_update_diagnosis.grid(row=1, column=0, columnspan=2, pady=10)

    # Method to update patient diagnosis
    def update_diagnosis(self, aadhar_no, diagnosis, update_diagnosis_window):
        if aadhar_no:
            try:
                self.patient_system.update_patient(aadhar_no, diagnosis)
                messagebox.showinfo("Success", "Diagnosis updated successfully!")
                self.update_patient_list()  # Updating patient list after updating diagnosis
                update_diagnosis_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating diagnosis: {str(e)}")
        else:
            messagebox.showerror("Error", "Please enter Aadhar Number.")

    # Method to fetch and display patient records
    def fetch_records(self):
        records = self.patient_system.get_patient_records()
        self.display_records(records)

    # Method to display patient records in a message box
    def display_records(self, records):
        if records:
            record_str = ""
            for record in records:
                record_str += f"ID: {record[0]}, Name: {record[1]}, DOB: {record[2]}, Diagnosis: {record[3]}, Admission Date: {record[4]}\n"
            messagebox.showinfo("Patient Records", record_str)
        else:
            messagebox.showinfo("Patient Records", "No records found.")

    # Method to update the patient list in the UI
    def update_patient_list(self):
        self.patient_listbox.delete(0, tk.END)
        records = self.patient_system.get_patient_records()
        for record in records:
            self.patient_listbox.insert(tk.END, (record[0], record[1]))

    # Placeholder method for future implementation (e.g., fetch additional details for the selected patient)
    def on_patient_select(self, event):
        pass

# Class for managing the Patient Record System data and interactions with the database
class PatientRecordSystem:
    # Initializing the database connection and creating the patient table
    def __init__(self, db_name="patient_records.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    # Method to create the patient table in the database if it doesn't exist
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS patient (
                    aadhar_no TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    diagnosis TEXT,
                    admission_date TEXT
                )
            ''')

    # Method to add a new patient to the database
    def add_patient(self, aadhar_no, name, dob, diagnosis=None):
        admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute('''
                INSERT INTO patient (aadhar_no, name, dob, diagnosis, admission_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (aadhar_no, name, dob, diagnosis, admission_date))

    # Method to update a patient's diagnosis in the database
    def update_patient(self, aadhar_no, diagnosis):
        with self.conn:
            self.conn.execute('''
                UPDATE patient
                SET diagnosis = ?
                WHERE aadhar_no = ?
            ''', (diagnosis, aadhar_no))

    # Method to retrieve all patient records from the database
    def get_patient_records(self):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT aadhar_no, name, dob, diagnosis, admission_date
                FROM patient
            ''')
            return cursor.fetchall()

    
# uses
root = tk.Tk()
app = PatientRecordSystemGUI(root)
root.mainloop()
