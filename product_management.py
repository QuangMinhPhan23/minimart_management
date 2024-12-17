import os
import shutil
import mysql.connector
server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = '27052306aA$'
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd, use_unicode=True, charset="utf8")
cur = conn.cursor()

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QVBoxLayout,
    QHBoxLayout, QWidget, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import helper_functions  # External helper functions (e.g., for QR, PDF handling)


class ProductManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        # Database connection
        self.server = '127.0.0.1'
        self.db = 'minimart'
        self.username = 'root'
        self.password = '27052306aA$'
        self.conn = mysql.connector.connect(
            host=self.server, database=self.db, user=self.username, password=self.password,
            use_unicode=True, charset="utf8"
        )
        self.cur = self.conn.cursor()

        # Data containers
        self.data_values = []
        self.selected_row = None

        # Initialize UI
        self.init_ui()

        # Load initial data
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Product Management")
        self.setGeometry(100, 100, 1000, 600)

        # Widgets for product information
        self.product_id_input = QLineEdit(self)
        self.product_id_input.setReadOnly(True)
        self.product_name_input = QLineEdit(self)
        self.origin_input = QLineEdit(self)
        self.file_input = QLineEdit(self)
        self.available_quantity_input = QLineEdit(self)

        # File browse button
        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)

        # Buttons for actions
        add_button = QPushButton("Add Row", self)
        add_button.clicked.connect(self.add_row)
        self.save_button = QPushButton("Save Edit", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_edit)
        delete_button = QPushButton("Delete Row", self)
        delete_button.clicked.connect(self.delete_row)
        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset_form)
        self.export_button = QPushButton("Export to PDF", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.pdf_extract)
        qr_button = QPushButton("QR Scan", self)
        qr_button.clicked.connect(self.qr_scan)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # Image display
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(200, 200)
        self.image_label.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Product table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Product ID', 'Name', 'Origin', 'Image', 'Available Quantity'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.select_row)

        # Layouts
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.product_id_input)
        form_layout.addWidget(QLabel("Product Name"))
        form_layout.addWidget(self.product_name_input)
        form_layout.addWidget(QLabel("Origin"))
        form_layout.addWidget(self.origin_input)
        form_layout.addWidget(QLabel("Image File"))
        form_layout.addWidget(self.file_input)
        form_layout.addWidget(browse_button)
        form_layout.addWidget(QLabel("Available Quantity"))
        form_layout.addWidget(self.available_quantity_input)

        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(qr_button)
        button_layout.addWidget(self.exit_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        central_layout = QVBoxLayout()
        central_layout.addLayout(main_layout)
        central_layout.addLayout(table_layout)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        """Load data from the database into the table."""
        query = "SELECT * FROM product ORDER BY ordinal_num ASC"
        self.cur.execute(query)
        self.data_values = helper_functions.table_read(conn, query, 1, 6)
        

        self.table.setRowCount(len(self.data_values))
        for row_index, row_data in enumerate(self.data_values):
            for col_index, value in enumerate(row_data):  # Skip ordinal_num
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def browse_file(self):
        """Open a file dialog to select an image."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.png *.jpeg)")
        if file_path:
            self.file_input.setText(file_path)
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def reset_form(self):
        """Reset the input form."""
        self.product_id_input.clear()
        self.product_name_input.clear()
        self.origin_input.clear()
        self.file_input.clear()
        self.available_quantity_input.clear()
        self.image_label.clear()
        self.save_button.setEnabled(False)
        self.export_button.setEnabled(False)

    def add_row(self):
        """Add a new row to the database and update the table."""
        product_id = helper_functions.create_product_id(self.data_values)
        product_name = self.product_name_input.text()
        origin = self.origin_input.text()
        file_path = self.file_input.text()
        available_quantity = self.available_quantity_input.text()

        if not product_name or not origin or not file_path or not available_quantity:
            QMessageBox.warning(self, "Warning", "All fields are required.")
            return

        # Save the file
        work_directory = os.getcwd()
        destination_folder = os.path.join(work_directory, "images_products")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        file_name = os.path.basename(file_path)
        if not helper_functions.file_excist(file_name, destination_folder):
            shutil.copy(file_path, destination_folder)
        self.cur.reset()
       
        sql="INSERT INTO product (ordinal_num,product_id,product_name,origin,image, available_quantity) VALUES (Null,'"
        sql+=product_id+"','"+product_name+"','"+origin+"','"+file_name+"','"+available_quantity+"');"    
        self.cur.execute(sql)
        self.conn.commit()
        QMessageBox.information(self, "Success", "Product added successfully!")
        # Refresh the table
        self.load_data()
        self.reset_form()

    def select_row(self, row, column):
        self.selected_row = row
        self.product_id_input.setText(self.table.item(row, 0).text())
        self.product_name_input.setText(self.table.item(row, 1).text())
        self.origin_input.setText(self.table.item(row, 2).text())
        self.file_input.setText(self.table.item(row, 3).text())
        self.available_quantity_input.setText(self.table.item(row, 4).text())
        self.save_button.setEnabled(True)
        self.export_button.setEnabled(True)

        # Load image
        work_directory = os.getcwd()
        image_path = os.path.join(work_directory, "images_products", self.table.item(row, 3).text())
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        else:
            self.image_label.clear()

    def save_edit(self):
        if self.selected_row is None:
            QMessageBox.warning(self, "Warning", "No row selected.")
            return

        product_id = self.product_id_input.text()
        product_name = self.product_name_input.text()
        origin = self.origin_input.text()
        file_path = self.file_input.text()
        available_quantity = self.available_quantity_input.text()

        if not product_name or not origin or not file_path or not available_quantity:
            QMessageBox.warning(self, "Warning", "All fields are required.")
            return

        # Save updated file
        work_directory = os.getcwd()
        destination_folder = os.path.join(work_directory, "images_products")
        file_name = os.path.basename(file_path)
        if not helper_functions.file_excist(file_name, destination_folder):
            shutil.copy(file_path, destination_folder)
        self.cur.reset()
        # Update in database
        query = f"""
        UPDATE product
        SET product_name='{product_name}', origin='{origin}', image='{file_name}', available_quantity='{available_quantity}'
        WHERE product_id='{product_id}'
        """
        QMessageBox.information(self, "Success", "Product updated successfully!")
        self.cur.execute(query)
        self.conn.commit()

        # Refresh the table
        self.load_data()
        self.reset_form()

    def delete_row(self):
        """Delete the selected row."""
        if self.selected_row is None:
            QMessageBox.warning(self, "Warning", "No row selected.")
            return
        self.cur.reset()
        product_id = self.table.item(self.selected_row, 0).text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete product {product_id}?",
                                        QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            query = f"DELETE FROM product WHERE product_id='{product_id}'"
            self.cur.execute(query)
            self.conn.commit()
            QMessageBox.information(self, "Success", "Product deleted successfully!")
            # Refresh the table
            self.load_data()
            self.reset_form()

    def pdf_extract(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "No row selected!")
            return
        else:     
            
            product_id = self.product_id_input.text()
            product_name = self.product_name_input.text()
            origin = self.origin_input.text()
            file_path = self.file_input.text()
            available_quantity = self.available_quantity_input.text()       
            helper_functions.QR_generate(product_id,product_name,origin,file_path,available_quantity)
            helper_functions.PDF_extract_product(product_id,product_name,origin,'qr_code.png',file_path, available_quantity)

    def qr_scan(self):
        maso=helper_functions.QR_trace()
        for nv in self.data_values:
            if nv[0]==maso:
                row = nv
        self.product_id_input.setText(row[0])
        self.product_name_input.setText(row[1])
        self.origin_input.setText(row[2])
        self.file_input.setText(row[3])
        self.available_quantity_input.setText(str(row[4]))
        self.save_button.setEnabled(True)
        self.export_button.setEnabled(True)


