# Category 1- UI development
#Task 2- Dynamic Data Display with Edit Functionality

#importing necessary libraries
import tkinter as tk
from tkinter import messagebox, simpledialog

# Creating the graphical user interface for the Patient Record
class PatientRecordSystemGUI:
    def __init__(self, master):
        # Initializing the main window
        self.master = master
        self.master.title("Patient Record Display")

        # Creating a list to store patient data
        self.patient_data = []

        # Creating and configuring UI components
        self.label_name = tk.Label(master, text="Name:")
        self.entry_name = tk.Entry(master)

        self.label_age = tk.Label(master, text="Age:")
        self.entry_age = tk.Entry(master)

        self.label_gender = tk.Label(master, text="Gender:")
        self.entry_gender = tk.Entry(master)

        self.label_phone = tk.Label(master, text="Phone:")
        self.entry_phone = tk.Entry(master)

        self.label_aadhar = tk.Label(master, text="Aadhar:")
        self.entry_aadhar = tk.Entry(master)

        self.button_add = tk.Button(master, text="Add Patient", command=self.add_patient)
        self.display_frame = tk.Frame(master)
        
        # Creating Grid layout for UI components
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_age.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_age.grid(row=1, column=1, padx=10, pady=5)

        self.label_gender.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_gender.grid(row=2, column=1, padx=10, pady=5)

        self.label_phone.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_phone.grid(row=3, column=1, padx=10, pady=5)

        self.label_aadhar.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_aadhar.grid(row=4, column=1, padx=10, pady=5)

        self.button_add.grid(row=5, column=0, columnspan=2, pady=10)

        self.display_frame.grid(row=6, column=0, columnspan=2, pady=10)

    def add_patient(self):
        # Getting patient details from entry fields
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        phone = self.entry_phone.get()
        aadhar = self.entry_aadhar.get()

        # Checking if all fields are filled
        if name and age and gender and phone and aadhar:
            # Adding patient data to the list and updating the display
            self.patient_data.append({"Name": name, "Age": age, "Gender": gender, "Phone": phone, "Aadhar": aadhar})
            self.update_display()
            self.clear_entries()
        else:
            # Displaying an error message if any field is empty
            messagebox.showerror("Error", "All fields are required.")

    def update_display(self):
        # Clearing previous entries in the display frame
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Displaying patient data with edit options
        for index, patient in enumerate(self.patient_data):
            label_text = f"{index + 1}. Name: {patient['Name']}, Age: {patient['Age']}, Gender: {patient['Gender']}, Phone: {patient['Phone']}, Aadhar: {patient['Aadhar']}"
            label = tk.Label(self.display_frame, text=label_text)
            label.grid(row=index, column=0, padx=10, pady=5, sticky=tk.W)

            edit_button = tk.Button(self.display_frame, text="Edit", command=lambda i=index: self.edit_patient(i))
            edit_button.grid(row=index, column=1, padx=10, pady=5)

    def edit_patient(self, index):
        # Fetching the patient data for the selected index
        patient = self.patient_data[index]

        # Displaying a dialog to edit patient details
        edited_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=patient['Name'])
        edited_age = simpledialog.askinteger("Edit Age", "Enter new age:", initialvalue=int(patient['Age']))
        edited_gender = simpledialog.askstring("Edit Gender", "Enter new gender:", initialvalue=patient['Gender'])
        edited_phone = simpledialog.askstring("Edit Phone", "Enter new phone number:", initialvalue=patient['Phone'])
        edited_aadhar = simpledialog.askstring("Edit Aadhar", "Enter new Aadhar number:", initialvalue=patient['Aadhar'])

        # Updating patient data with edited values
        self.patient_data[index] = {
            "Name": edited_name,
            "Age": str(edited_age),
            "Gender": edited_gender,
            "Phone": edited_phone,
            "Aadhar": edited_aadhar
        }

        # Updating the display after editing
        self.update_display()

    def clear_entries(self):
        # Clearing entry fields after adding a patient
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_aadhar.delete(0, tk.END)

#usage
root = tk.Tk()
app = PatientRecordSystemGUI(root)
root.mainloop()
