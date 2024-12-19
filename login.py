import sys
import helper_functions

import mysql.connector

# Connect to database
server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd, use_unicode=True, charset="utf8")
cur = conn.cursor()
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QMessageBox
import panel
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Form")
        self.setFixedSize(300, 200)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        layout = QVBoxLayout()

        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Forget password
        self.forget_password_label = QLabel("Forget password?")
        self.forget_password_label.setStyleSheet("color: blue; text-decoration: underline; cursor: pointer;")
        layout.addWidget(self.forget_password_label)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

        # Connect signals to slots
        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)
        self.forget_password_label.mousePressEvent = self.on_forget_password

    def on_submit(self):
        user = self.username_input.text()
        password = self.password_input.text()

        # Reading database to check if User and Pass are in the login table
        sql = 'SELECT * FROM login'
        User_list = helper_functions.table_read(conn, sql, 1, 3)
        for us in User_list:
            if user == us[0] and password == us[1]:
                QMessageBox.information(self, "Success", "Login successful!")
                self.close()
                # panel.panel_form()
                self.w = panel.ControlPanel()
                self.w.show()
                return
        QMessageBox.warning(self, "Error", "Incorrect username or password")

    def on_forget_password(self, event):
        QMessageBox.information(self, "Password Recovery", "Contact the admin for password recovery.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
