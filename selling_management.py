from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QRadioButton, 
    QWidget, QHeaderView, QSpinBox
)
from PyQt5.QtCore import Qt, QDate
from datetime import date
import helper_functions
import mysql.connector

class SellingManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management")
        self.setGeometry(100, 100, 1200, 800)
        
        # MySQL connection
        self.server = '127.0.0.1'
        self.db = 'minimart'
        self.username = 'root'
        self.pwd = '27052306aA$'
        self.conn = mysql.connector.connect(host=self.server, database=self.db, user=self.username, password=self.pwd)
        self.cur = self.conn.cursor()

        # Variables
        self.DataValues = []
        self.total = 0
        self.Keylist = ['ORDER', 'DATE', 'ITEMID', 'ITEM NAME', 'ORIGIN','AVAILABLE', 'UNIT PRICE','QUANTITY', 'AMOUNT','TOTAL']
        self.Headings = ['Order', 'Date', 'Item ID', 'Item name', 'Origin','Available', 'Unit price', 'Quantity', 'Amount']
        self.Headings1 = ['Order', 'Item ID', 'Item name', 'Origin', 'Unit price', 'Quantity', 'Amount']

        # UI Elements
        self.initUI()

    def initUI(self):
        # Create main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Panel for inputs
        input_panel = QFrame()
        panel_layout = QVBoxLayout()

        self.inputs = {}
        for heading, key in zip(self.Headings[:10], self.Keylist[:9]):
            row = QHBoxLayout()
            label = QLabel(heading)
            input_field = QLineEdit()
            input_field.setObjectName(key)
            if key in ['DATE', 'AVAILABLE', 'AMOUNT']:
                input_field.setReadOnly(True)
            row.addWidget(label)
            row.addWidget(input_field)
            self.inputs[key] = input_field
            panel_layout.addLayout(row)

        input_panel.setLayout(panel_layout)
        main_layout.addWidget(input_panel)

        # Buttons
        button_panel = QHBoxLayout()
        self.find_button = QPushButton("Find")
        self.pdf_button = QPushButton("PDF")
        self.delete_row_button = QPushButton("Delete Row")
        self.update_button = QPushButton("Update")
        self.reset_button = QPushButton("Reset")
        self.qr_scan_button = QPushButton("QR Scan")
        self.exit_button = QPushButton("Exit")

        button_panel.addWidget(self.find_button)
        button_panel.addWidget(self.pdf_button)
        button_panel.addWidget(self.delete_row_button)
        button_panel.addWidget(self.update_button)
        button_panel.addWidget(self.reset_button)
        button_panel.addWidget(self.qr_scan_button)
        button_panel.addWidget(self.exit_button)
        main_layout.addLayout(button_panel)
        
        # Total sum display
        total_layout = QHBoxLayout()
        total_label = QLabel("Total sum:")
        self.total_display = QLabel("0")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_display)
        main_layout.addLayout(total_layout)

        # Table
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.Headings1))
        self.table.setHorizontalHeaderLabels(self.Headings1)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        self.table.cellClicked.connect(self.table_row_selected)

        

        # Set main widget and layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Connect button actions
        self.find_button.clicked.connect(self.find_item)
        self.pdf_button.clicked.connect(self.generate_pdf)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.update_button.clicked.connect(self.update_row)
        self.reset_button.clicked.connect(self.reset_form)
        self.qr_scan_button.clicked.connect(self.qr_scan)
        self.exit_button.clicked.connect(self.close)
        
    def table_row_selected(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            self.selected_row_index = self.table.currentRow()
            row_data = self.DataValues[self.selected_row_index]
            # ['ORDER', 'DATE', 'ITEMID', 'ITEM NAME', 'ORIGIN', 'AVAILABLE', 'UNIT PRICE','QUANTITY', 'AMOUNT', 'TOTAL']
            self.inputs['ORDER'].setText(str(row_data[0]))
            self.inputs['DATE'].setText(QDate.currentDate().toString(Qt.ISODate))
            self.inputs['ITEMID'].setText(str(row_data[1]))
            self.inputs['ITEM NAME'].setText(str(row_data[2]))
            self.inputs['ORIGIN'].setText(str(row_data[3]))
            self.inputs['AVAILABLE'].setText(str(row_data[7]))
            self.inputs['UNIT PRICE'].setText(str(row_data[4]))
            self.inputs['QUANTITY'].setText(str(row_data[5]))
            self.inputs['AMOUNT'].setText(str(row_data[6]))

    def reset_form(self):
        for key, field in self.inputs.items():
            field.clear()
        self.total_display.setText("0")

    def qr_scan(self):
        item_id = helper_functions.QR_trace()
        sql = f"SELECT * FROM quotation WHERE product_id='{item_id}'"
        data1 = helper_functions.table_read(self.conn, sql, 1, 3)

        if not data1:
            QMessageBox.warning(self, "Error", "Item does not have a price ID")
            return

        price_id = data1[-1][0]
        sql = (f"SELECT quotation.product_id AS id, product_name, origin, price, available_quantity "
               f"FROM quotation, product WHERE quotation.product_id=product.product_id AND price_id='{price_id}'")
        Data = helper_functions.table_read(self.conn, sql, 0, 5)

        if not Data:
            QMessageBox.warning(self, "Error", "No data found for the scanned QR code")
            return

        Data_row = Data[0]
        Data_row.insert(0, len(self.DataValues) + 1)  # Insert num column
        Data_row.insert(5, 1)  # Quantity column
        Data_row.insert(6, int(Data_row[4]))  # Amount column

        # Add to DataValues and update total
        self.DataValues.append(Data_row)
        self.update_total()

        # Update table
        self.update_table()

    def find_item(self):
        try:
            item_id = self.inputs['ITEMID'].text()

            sql = f"SELECT * FROM quotation WHERE product_id='{item_id}'"
            data1 = helper_functions.table_read(self.conn, sql, 1, 3)

            if not data1:
                QMessageBox.warning(self, "Error", "Item does not have a price ID")
                return

            price_id = data1[-1][0]
            sql = (f"SELECT quotation.product_id AS id, product_name, origin, price, available_quantity "
                f"FROM quotation, product WHERE quotation.product_id=product.product_id AND price_id='{price_id}'")
            Data = helper_functions.table_read(self.conn, sql, 0, 5)

            if not Data:
                QMessageBox.warning(self, "Error", "No data found for the scanned QR code")
                return

            Data_row = Data[0]
            Data_row.insert(0, len(self.DataValues) + 1)  # Insert num column
            Data_row.insert(5, 1)  # Quantity column
            Data_row.insert(6, int(Data_row[4]))  # Amount column

            # Add to DataValues and update total
            self.DataValues.append(Data_row)
            self.update_total()

            # Update table
            self.update_table()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error while querying database: {e}")

    def update_row(self):

        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a row to update.")
            return

        try:
            # Extract updated data from input fields
            updated_data = []
            for key in self.Keylist[:8]:
                value = self.inputs[key].text()
                updated_data.append(value)
            # Compute the 'AMOUNT' field as Quantity * Unit Price
            total = int(updated_data[6]) * int(updated_data[7])
            
            new_data = []
            new_data.append(int(updated_data[0]))
            new_data.append(updated_data[2])
            new_data.append(updated_data[3])
            new_data.append(updated_data[4])
            new_data.append(updated_data[6])
            new_data.append(int(updated_data[7]))
            new_data.append(total)
            new_data.append(int(updated_data[5]))
            # Update the DataValues list and table
            self.DataValues[selected_row] = new_data
            self.update_total()
            self.update_table()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please ensure all fields are filled out correctly.")

    def delete_row(self):
        """
        Deletes the selected row from the table and updates totals.
        """
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return

        # Remove row from DataValues and table
        self.DataValues.pop(selected_row)
        self.update_table()
        self.update_total()


    def generate_pdf(self):
        try:
            today = date.today()
            order_id = helper_functions.create_order_id(self.conn)
            sql="INSERT INTO selling (ordinal_num,order_id,date, Amount) VALUES (Null,'"+str(order_id)+"','"+str(today)+"','"+str(self.total)+"')"
            self.cur.execute(sql)
            for row in self.DataValues:
                sub=row[5]-int(row[7])
                sql="UPDATE product SET available_quantity='"+str(sub)+"'WHERE product_id='"+row[1]+"';"
                self.cur.execute(sql)
            
            helper_functions.PDF_extract_selling(self.DataValues,order_id,str(today),str(self.total))
            self.reset_form()
            self.DataValues = []
            self.update_table()
            self.update_total()
            QMessageBox.information(self, "Success", f"PDF generated successfully at receipt.pdf")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {e}")

    def update_table(self):
        
        self.table.setRowCount(len(self.DataValues))
        for i, row in enumerate(self.DataValues):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def update_total(self):

        self.total = sum(row[6] for row in self.DataValues)  # Sum of the 'Amount' column
        self.total_display.setText(str(self.total))

