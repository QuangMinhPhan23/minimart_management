import mysql.connector
import helper_functions
import os
import shutil

# Database Connection Configuration
server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = '27052306aA$'
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd, use_unicode=True, charset="utf8")
cur = conn.cursor()
from PyQt5 import QtWidgets, QtGui, QtCore
class QuotationManagement(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quotation Management")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
        self.load_data()

    def initUI(self):
        # Layouts
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Input Fields
        self.inputs_layout = QtWidgets.QGridLayout()

        self.product_id_label = QtWidgets.QLabel("Product ID:")
        self.product_id_input = QtWidgets.QLineEdit()
        self.inputs_layout.addWidget(self.product_id_label, 0, 0)
        self.inputs_layout.addWidget(self.product_id_input, 0, 1)

        self.price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QLineEdit()
        self.inputs_layout.addWidget(self.price_label, 1, 0)
        self.inputs_layout.addWidget(self.price_input, 1, 1)

        self.date_label = QtWidgets.QLabel("Applied Date:")
        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.inputs_layout.addWidget(self.date_label, 2, 0)
        self.inputs_layout.addWidget(self.date_input, 2, 1)

        self.supplier_label = QtWidgets.QLabel("Supplier:")
        self.supplier_input = QtWidgets.QLineEdit()
        self.inputs_layout.addWidget(self.supplier_label, 3, 0)
        self.inputs_layout.addWidget(self.supplier_input, 3, 1)

        self.add_row_button = QtWidgets.QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        self.inputs_layout.addWidget(self.add_row_button, 4, 0)

        self.delete_row_button = QtWidgets.QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)
        self.inputs_layout.addWidget(self.delete_row_button, 4, 1)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_form)
        self.inputs_layout.addWidget(self.reset_button, 4, 2)

        self.save_edit_button = QtWidgets.QPushButton("Save Edit")
        self.save_edit_button.clicked.connect(self.save_edit)
        self.inputs_layout.addWidget(self.save_edit_button, 4, 3)
        
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.inputs_layout.addWidget(self.exit_button, 4, 4)
        
        self.pdf_button = QtWidgets.QPushButton("PDF Extract")
        self.pdf_button.clicked.connect(self.pdf_extract)
        self.inputs_layout.addWidget(self.pdf_button, 4, 5)
        
        self.qr_button = QtWidgets.QPushButton("QR Scan")
        self.qr_button.clicked.connect(self.qr_scan)
        self.inputs_layout.addWidget(self.qr_button, 4, 6)

        self.main_layout.addLayout(self.inputs_layout)

        # Table for displaying data
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Price ID", "Product ID", "Price", "Applied Date", "Supplier"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.on_table_select)
        self.main_layout.addWidget(self.table)

    def load_data(self):
        """Load data from the database into the table"""
        sql = 'SELECT * FROM quotation ORDER BY ordinal_num ASC'
        self.data = helper_functions.table_read(conn, sql, 1, 6)

        self.table.setRowCount(len(self.data))
        for row_idx, row_data in enumerate(self.data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col_data)))

    def add_row(self):
        """Add a new row to the database and refresh the table"""
        product_id = self.product_id_input.text()
        price = self.price_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        supplier = self.supplier_input.text()

        if not product_id or not price or not supplier:
            QtWidgets.QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        price_id = helper_functions.create_price_id(self.data)

        sql = """
        INSERT INTO quotation (ordinal_num, price_id, product_id, price, Applied_date, supplier)
        VALUES (NULL, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (price_id, product_id, price, date, supplier))
        conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Product added successfully!")
        self.load_data()
        self.reset_form()

    def delete_row(self):
        """Delete the selected row from the database and refresh the table"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Warning", "No row selected!")
            return

        price_id = self.table.item(selected_row, 0).text()

        sql = "DELETE FROM quotation WHERE price_id = %s"
        cur.execute(sql, (price_id,))
        conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Product deleted successfully!")
        self.load_data()

    def save_edit(self):
        """Save the edited row to the database and refresh the table"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Warning", "No row selected!")
            return

        price_id = self.table.item(selected_row, 0).text()
        product_id = self.product_id_input.text()
        price = self.price_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        supplier = self.supplier_input.text()

        if not product_id or not price or not supplier:
            QtWidgets.QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        sql = """
        UPDATE quotation
        SET product_id = %s, price = %s, Applied_date = %s, supplier = %s
        WHERE price_id = %s
        """
        cur.execute(sql, (product_id, price, date, supplier, price_id))
        conn.commit()
        QtWidgets.QMessageBox.information(self, "Success", "Product updated successfully!")
        self.load_data()
        self.reset_form()

    def reset_form(self):
        """Clear the input fields"""
        self.product_id_input.clear()
        self.price_input.clear()
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.supplier_input.clear()

    def on_table_select(self):
        """Populate the input fields with the selected table row's data"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        self.product_id_input.setText(self.table.item(selected_row, 1).text())
        self.price_input.setText(self.table.item(selected_row, 2).text())
        self.date_input.setDate(QtCore.QDate.fromString(self.table.item(selected_row, 3).text(), "yyyy-MM-dd"))
        self.supplier_input.setText(self.table.item(selected_row, 4).text())
        
    def pdf_extract(self):
        row = self.table.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "No row selected!")
            return
        else:     
            
            price_id = self.table.item(row, 0).text()
            product_id = self.product_id_input.text()
            price = self.price_input.text()
            date = self.date_input.date().toString("yyyy-MM-dd")
            supplier = self.supplier_input.text()     
            helper_functions.QR_generate(price_id,product_id,price,date,supplier)
            helper_functions.PDF_extract_quotation(price_id,product_id,price,'qr_code.png',date, supplier)
            
    def qr_scan(self):
        maso=helper_functions.QR_trace()
        for nv in self.data:
            if nv[0]==maso:
                row = nv
        self.product_id_input.setText(row[1])
        self.price_input.setText(row[2])
        self.date_input.setDate(QtCore.QDate.fromString(str(row[3]), "yyyy-MM-dd"))
        self.supplier_input.setText(row[4])
        self.save_edit_button.setEnabled(True)
        self.pdf_button.setEnabled(True)

