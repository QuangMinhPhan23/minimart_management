import os
import shutil
import sys
# from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDate
import mysql.connector
import helper_functions

server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = '27052306aA$'
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd, use_unicode=True, charset="utf8")
cur = conn.cursor()
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QRadioButton, 
                             QFileDialog, QMessageBox, QDateEdit, )


class StaffManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Staff Management")
        self.setGeometry(100, 100, 800, 600)

        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.button_layout = QHBoxLayout()
        self.table_layout = QVBoxLayout()

        # Form Fields
        self.staff_id = QLineEdit()
        self.staff_id.setPlaceholderText("Staff ID")
        self.staff_id.setReadOnly(True)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")

        self.date_of_birth = QDateEdit()
        self.date_of_birth.setCalendarPopup(True)  # Enable calendar popup
        self.date_of_birth.setDisplayFormat("yyyy-MM-dd")  # Format the date
        # self.date_of_birth.setPlaceholderText("Date of Birth (YYYY-MM-DD)")

        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")

        self.id_number = QLineEdit()
        self.id_number.setPlaceholderText("ID Number")

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone Number")

        self.file_button = QPushButton("Upload Image")
        self.file_button.clicked.connect(self.upload_image)

        self.image_path = QLineEdit()
        self.image_path.setReadOnly(True)

        # Add form fields to layout
        self.form_layout.addRow(QLabel("Staff ID:"), self.staff_id)
        self.form_layout.addRow(QLabel("Name:"), self.name)
        self.form_layout.addRow(QLabel("Date of Birth:"), self.date_of_birth)
        self.form_layout.addRow(QLabel("Gender:"), self.gender_male)
        self.form_layout.addRow("", self.gender_female)
        self.form_layout.addRow(QLabel("ID Number:"), self.id_number)
        self.form_layout.addRow(QLabel("Phone Number:"), self.phone_number)
        self.form_layout.addRow(QLabel("Image:"), self.image_path)
        self.form_layout.addRow("", self.file_button)

        # Buttons
        self.add_button = QPushButton("Add Row")
        self.add_button.clicked.connect(self.add_row)

        self.edit_button = QPushButton("Save Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.save_edit)

        self.delete_button = QPushButton("Delete Row")
        self.delete_button.clicked.connect(self.delete_row)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_form)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        
        self.qr_button = QPushButton("QR Scan")
        self.qr_button.clicked.connect(self.qr_scan)
        
        self.pdf_button = QPushButton("PDF Extract")
        self.pdf_button.clicked.connect(self.pdf_extract)

        # Add buttons to layout
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.exit_button)
        self.button_layout.addWidget(self.qr_button)
        self.button_layout.addWidget(self.pdf_button)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Staff ID", "Name", "Date of Birth", "Gender", "ID Number", "Phone Number", "Image"])
        self.table.cellClicked.connect(self.table_row_selected)

        self.table_layout.addWidget(self.table)

        # Combine layouts
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.table_layout)

        self.central_widget.setLayout(self.main_layout)

        # Load initial data
        self.load_data()

    def load_data(self):
        sql = 'SELECT * FROM staff ORDER BY ordinal_num ASC'
        self.data = helper_functions.table_read(conn, sql, 1, 8)

        self.table.setRowCount(len(self.data))
        for row_index, row_data in enumerate(self.data):
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.png)")
        if file_path:
            self.image_path.setText(file_path)

    def add_row(self):
        sql = 'SELECT * FROM staff ORDER BY ordinal_num ASC'
        self.data = helper_functions.table_read(conn, sql, 1, 8)
        name = self.name.text()
        date_of_birth = self.date_of_birth.text()
        gender = "Male" if self.gender_male.isChecked() else "Female"
        id_number = self.id_number.text()
        phone_number = self.phone_number.text()
        image_path = self.image_path.text()

        # Validation
        if not name or not date_of_birth or not id_number or not phone_number or not image_path:
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return

        # Add to table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem("Auto"))  # Staff ID (auto-generated)
        self.table.setItem(row_position, 1, QTableWidgetItem(name))
        self.table.setItem(row_position, 2, QTableWidgetItem(date_of_birth))
        self.table.setItem(row_position, 3, QTableWidgetItem(gender))
        self.table.setItem(row_position, 4, QTableWidgetItem(id_number))
        self.table.setItem(row_position, 5, QTableWidgetItem(phone_number))
        self.table.setItem(row_position, 6, QTableWidgetItem(os.path.basename(image_path)))
        id_num = helper_functions.create_staff_id(self.data)
        if gender == 'Male':
            gender_id = 1
        else:
            gender_id = 0
        # Save to database
        sql = "INSERT INTO staff (ordinal_num, staff_id, staff_name, date_of_birth, gender, identification, mobile_phone, image) VALUES (Null, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (id_num, name, date_of_birth, gender_id, id_number, phone_number, os.path.basename(image_path)))
        conn.commit()

        QMessageBox.information(self, "Success", "Staff added successfully!")
        self.reset_form()

    def reset_form(self):
        self.staff_id.clear()
        self.name.clear()
        self.gender_male.setChecked(True)
        self.id_number.clear()
        self.phone_number.clear()
        self.image_path.clear()
        self.edit_button.setEnabled(False)

    def table_row_selected(self, row, column):
        self.edit_button.setEnabled(True)

        self.staff_id.setText(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        # self.date_of_birth.setDate(self.table.item(row, 2))
        date_of_birth_str = self.table.item(row, 2).text()
        self.date_of_birth.setDate(QDate.fromString(date_of_birth_str, "yyyy-MM-dd"))
        gender = self.table.item(row, 3).text()
        self.gender_male.setChecked(gender == '1')
        self.gender_female.setChecked(gender == '0')
        self.id_number.setText(self.table.item(row, 4).text())
        self.phone_number.setText(self.table.item(row, 5).text())
        self.image_path.setText(self.table.item(row, 6).text())

    def save_edit(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "No row selected!")
            return

        # Update data
        self.table.setItem(row, 1, QTableWidgetItem(self.name.text()))
        # date_of_birth = self.date_of_birth.text()
        self.table.setItem(row, 2, QTableWidgetItem(str(self.date_of_birth)))
        gender = 1 if self.gender_male.isChecked() else 0
        self.table.setItem(row, 3, QTableWidgetItem(gender))
        self.table.setItem(row, 4, QTableWidgetItem(self.id_number.text()))
        self.table.setItem(row, 5, QTableWidgetItem(self.phone_number.text()))
                # Save changes to the database
        staff_id = self.staff_id.text()
        name = self.name.text()
        date_of_birth = self.date_of_birth.date().toString("yyyy-MM-dd")
        id_number = self.id_number.text()
        phone_number = self.phone_number.text()
        image_path = self.image_path.text()

        # Validation
        if not staff_id:
            QMessageBox.warning(self, "Warning", "Staff ID is missing!")
            return

        try:
            sql = """UPDATE staff 
                     SET staff_name = %s, date_of_birth = %s, gender = %s, 
                         identification = %s, mobile_phone = %s, image = %s
                     WHERE staff_id = %s"""
            cur.execute(sql, (name, date_of_birth, gender, id_number, phone_number, 
                              os.path.basename(image_path), staff_id))
            conn.commit()
            QMessageBox.information(self, "Success", "Staff information updated successfully!")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Failed to update data: {err}")
        finally:
            self.reset_form()

    def delete_row(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "No row selected!")
            return

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                     "Are you sure you want to delete this staff member?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        staff_id = self.table.item(row, 0).text()
        if not staff_id:
            QMessageBox.warning(self, "Warning", "Staff ID is missing!")
            return

        try:
            sql = "DELETE FROM staff WHERE staff_id = %s"
            cur.execute(sql, (staff_id,))
            conn.commit()

            self.table.removeRow(row)
            QMessageBox.information(self, "Success", "Staff member deleted successfully!")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Failed to delete data: {err}")
        finally:
            self.reset_form()
            
    def qr_scan(self):
        maso=helper_functions.QR_trace()
        for nv in self.data:
            if nv[0]==maso:
                row = nv
        self.staff_id.setText(row[0])
        self.name.setText(row[1])
        date_of_birth_str = str(row[2])
        self.date_of_birth.setDate(QDate.fromString(date_of_birth_str, "yyyy-MM-dd"))
        gender = str(row[3])
        self.gender_male.setChecked(gender == '1')
        self.gender_female.setChecked(gender == '0')
        self.id_number.setText(row[4])
        self.phone_number.setText(row[5])
        self.image_path.setText(row[6])
       
            
    def pdf_extract(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "No row selected!")
            return
        else:     
            staff_id = self.staff_id.text()      
            name = self.name.text()
            date_of_birth = self.date_of_birth.date().toString("yyyy-MM-dd")
            id_number = self.id_number.text()
            phone_number = self.phone_number.text()
            image_path = self.image_path.text()           
            helper_functions.QR_generate(staff_id,name,date_of_birth,id_number,image_path)
            helper_functions.PDF_extract_staff(name,date_of_birth,phone_number,id_number,'qr_code.png',image_path)