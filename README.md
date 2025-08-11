# Minimart Managemnet

Simulating a simplified management system for a minimart using Python, PyQt5 for GUI and MySQL for database. (See branch **PySimpleGUI-version** for PySimpleGUI as GUI)
Minimart Management System Simulation

<img width="541" height="341" alt="image" src="https://github.com/user-attachments/assets/0901ef3d-0dd8-4170-9c33-091ed53a045f" />

<img width="362" height="294" alt="image" src="https://github.com/user-attachments/assets/87e97ae2-f69a-4070-a56e-414120f633f3" />

<img width="865" height="633" alt="image" src="https://github.com/user-attachments/assets/34866d3a-9a49-4fee-96ee-9aaadf04c1ae" />

<img width="838" height="575" alt="image" src="https://github.com/user-attachments/assets/bc3d56f7-4a24-4241-850d-6303d1106350" />

<img width="992" height="642" alt="image" src="https://github.com/user-attachments/assets/2d5b91e2-3bfb-4c58-b738-ec344d6fbd77" />
## Description

This project is a Minimart Management System Simulation built with Python, utilizing PyQt5 for the graphical user interface and MySQL for database management. It provides functionalities for managing staff, products, quotations, and selling processes in a streamlined and user-friendly manner.

## Features

### Login Panel

* Execute login.py to access the system.

* Enter your username and password and press Submit.

* panel.py will be accessed and show options to manage staff, products, quotations, and selling.

### Staff Management

* **Add Row:** Fill in staff details and press Add Row (ID must be 10 characters, and phone numbers should start with 0 followed by 9 digits).

* **Delete Row:** Select a staff entry and press Delete Row to remove it.

* **Save Edit:** Select a staff entry, edit the details, and press Save Edit to update.

* **Reset:** Clear all input fields.

* **PDF Extract:** Generate a PDF file containing the selected staff's details and a QR code.

* **QR Scan:** Use the camera to scan a QR code and automatically fill in staff details.

* **Exit:** Close the staff management window and return to the main panel.

### Product, Quotation, and Selling Management

Functions similar to staff management but adapted for their respective purposes.

### Selling Management Specifics

* **Find:** Enter a product_id (e.g., SP003 or SP002) in the Item ID field and press Find to automatically add the item.

* **QR Scan:** Use the camera to scan a product QR code (generated in the PDF Extract of a product).

* **Update:** Edit order details, and the total price will automatically update.

* **PDF Extract:** Generate a receipt PDF with receipt details and all purchased items.

## Installation and Setup

### Prerequisites

* Python installed on your system.

* MySQL installed and configured.

### Steps

* Install the required Python packages.

* Create a MySQL account and a database.

* Name your database (default is minimart).

* Inside the database, create the following tables:

   * staff

   * product

   * quotation

   * selling

* A separate table for login credentials.

* Use the SQL script minimart.sql to set up the database structure and populate it with example data.

* Run the SQL script in your MySQL query editor.

* Start the application.

* python login.py

* Log in with your username and password and access the main panel.

## File Descriptions

* **login.py:** Handles user login and authentication.

* **panel.py:** The main dashboard for accessing different management modules.

* **staff_management.py, product_management.py, quotation_management.py, and selling_management.py:** Individual modules for managing respective data.

* **minimart.sql:** SQL script to create and populate the database.

* **helper_functions.py:** Utility functions to support database operations, PDF generation, and QR code handling.

## Dependencies

* PyQt5

* MySQL Connector for Python

* ReportLab (for PDF generation)

* OpenCV (for QR scanning)

## Acknowledgments

This project simulates a real-world minimart management system, providing hands-on experience in GUI development, database integration, and functional programming. It serves as an excellent foundation for expanding to more advanced inventory and sales tracking systems.
