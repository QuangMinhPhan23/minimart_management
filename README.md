# Minimart Managemnet

Simulating a simplified management system for a minimart using Python, PyQt5 for GUI and MySQL for database. (See branch **PySimpleGUI-version** for PySimpleGUI as GUI)
Minimart Management System Simulation

## Description

This project is a Minimart Management System Simulation built with Python, utilizing PyQt5 for the graphical user interface and MySQL for database management. It provides functionalities for managing staff, products, quotations, and selling processes in a streamlined and user-friendly manner.

## Features

### Login Panel

* Execute login.py to access the system.

* Enter your username and password and press Submit.

* panel.py will be accessed and show options to manage staff, products, quotations, and selling.

### Staff Management

* Add Row: Fill in staff details and press Add Row (ID must be 10 characters, and phone numbers should start with 0 followed by 9 digits).

* Delete Row: Select a staff entry and press Delete Row to remove it.

* Save Edit: Select a staff entry, edit the details, and press Save Edit to update.

* Reset: Clear all input fields.

* PDF Extract: Generate a PDF file containing the selected staff's details and a QR code.

* QR Scan: Use the camera to scan a QR code and automatically fill in staff details.

* Exit: Close the staff management window and return to the main panel.

### Product, Quotation, and Selling Management

Functions similar to staff management but adapted for their respective purposes.

### Selling Management Specifics

* Find: Enter a product_id (e.g., SP003 or SP002) in the Item ID field and press Find to automatically add the item.

* QR Scan: Use the camera to scan a product QR code (generated in the PDF Extract of a product).

* Update: Edit order details, and the total price will automatically update.

* PDF Extract: Generate a receipt PDF with receipt details and all purchased items.

## Installation and Setup

### Prerequisites

* Python installed on your system.

* MySQL installed and configured.

### Steps

* Install the required Python packages.

* pip install -r requirements.txt

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

* login.py: Handles user login and authentication.

* panel.py: The main dashboard for accessing different management modules.

* staff_management.py, product_management.py, quotation_management.py, and selling_management.py: Individual modules for managing respective data.

* minimart.sql: SQL script to create and populate the database.

* helper_functions.py: Utility functions to support database operations, PDF generation, and QR code handling.

## Usage

### Workflow

* Start with login.py to authenticate.

* Use the Panel to navigate to the desired management module.

* Perform actions such as adding, updating, deleting, and extracting data as PDFs with QR codes.

* In the Selling Management module, generate receipts and track purchases.

### Notes

Ensure database configurations in the script (e.g., server, username, password) match your local setup.

All required table schemas and example data are provided in minimart.sql.

## Database Configuration

Default Settings:

Server: 127.0.0.1

Database: minimart

Username: root

Password: 

Modify these values in the scripts if your setup is different.

## Example Data

* The minimart.sql file contains:

* Sample data for staff, product, quotation, and selling tables.

* Login table with example credentials.

## Dependencies

* PyQt5

* MySQL Connector for Python

* ReportLab (for PDF generation)

* OpenCV (for QR scanning)

## Acknowledgments

This project simulates a real-world minimart management system, providing hands-on experience in GUI development, database integration, and functional programming. It serves as an excellent foundation for expanding to more advanced inventory and sales tracking systems.
