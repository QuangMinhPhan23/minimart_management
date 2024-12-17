import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import staff_management
import product_management
import selling_management
import quotation_management

class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setFixedSize(300, 200)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        self.selling_button = QPushButton("Selling Management")
        self.staff_button = QPushButton("Staff Management")
        self.inventory_button = QPushButton("Product Management")
        self.quotation_button = QPushButton("Quotation Management")

        # Add buttons to layout
        layout.addWidget(self.selling_button)
        layout.addWidget(self.staff_button)
        layout.addWidget(self.inventory_button)
        layout.addWidget(self.quotation_button)
        
        # Connect signals to slots
        self.selling_button.clicked.connect(self.open_selling_management)
        self.staff_button.clicked.connect(self.open_staff_management)
        self.inventory_button.clicked.connect(self.open_product_management)
        self.quotation_button.clicked.connect(self.open_quotation_management)
        
        central_widget.setLayout(layout)

    def open_selling_management(self):
        self.w = selling_management.SellingManagement()
        self.w.show()


    def open_staff_management(self):
        self.w = staff_management.StaffManagement()
        self.w.show()

    def open_product_management(self):
        self.w = product_management.ProductManagement()
        self.w.show()

    def open_quotation_management(self):
        self.w = quotation_management.QuotationManagement()
        self.w.show()

      


