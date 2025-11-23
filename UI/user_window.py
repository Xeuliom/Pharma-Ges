from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QSpinBox, QMessageBox, QGroupBox, QHeaderView, QAbstractItemView
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.db_setup import Medicine, Customer, Sale
from datetime import datetime
import os


engine = create_engine("sqlite:///pharmacy.db")
Session = sessionmaker(bind=engine)
session = Session()

class UserWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.log_file = f"sales_logs/{datetime.now().strftime('%Y-%m-%d')}_sales.txt"
        os.makedirs("sales_logs", exist_ok=True)
        
        self.setWindowTitle("Pharmacy User Dashboard")
        self.setGeometry(200, 200, 800, 600)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medicine by name...")
        self.search_input.textChanged.connect(self.load_medicines)

        # Medicine table
        self.medicine_table = QTableWidget()
        self.medicine_table.setColumnCount(5)
        self.medicine_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Expiry"])
        self.medicine_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.medicine_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Quantity and customer info
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)

        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Customer Name")

        self.customer_phone_input = QLineEdit()
        self.customer_phone_input.setPlaceholderText("Customer Phone")

        self.sell_button = QPushButton("Sell Medicine")
        self.sell_button.clicked.connect(self.handle_sale)

        # Back to login button
        self.back_button = QPushButton("Back to Admin Login")
        self.back_button.setStyleSheet("background-color: red; color: white;")
        self.back_button.clicked.connect(self.go_back_to_login)

        # Layouts
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Quantity"))
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(QLabel("Customer Name"))
        form_layout.addWidget(self.customer_name_input)
        form_layout.addWidget(QLabel("Customer Phone"))
        form_layout.addWidget(self.customer_phone_input)
        form_layout.addWidget(self.sell_button)

        form_box = QGroupBox("Sell Medicine")
        form_box.setLayout(form_layout)

        # Top bar with user label and back button
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Logged in as: Guest User"))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.search_input)
        layout.addWidget(self.medicine_table)
        layout.addWidget(form_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_medicines()

    def load_medicines(self):
        keyword = self.search_input.text().strip().lower()
        medicines = session.query(Medicine).all()

        if keyword:
            medicines = [m for m in medicines if keyword in m.name.lower()]

        self.medicine_table.setRowCount(len(medicines))
        for row, med in enumerate(medicines):
            self.medicine_table.setItem(row, 0, QTableWidgetItem(str(med.id)))
            self.medicine_table.setItem(row, 1, QTableWidgetItem(med.name))
            self.medicine_table.setItem(row, 2, QTableWidgetItem(f"{med.price:.2f}"))
            self.medicine_table.setItem(row, 3, QTableWidgetItem(str(med.quantity)))
            self.medicine_table.setItem(row, 4, QTableWidgetItem(
                med.expiry_date.strftime("%Y-%m-%d") if med.expiry_date else ""
            ))

    def handle_sale(self):
        row = self.medicine_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a medicine.")
            return

        med_id = int(self.medicine_table.item(row, 0).text())
        medicine = session.query(Medicine).get(med_id)
        quantity = self.quantity_input.value()

        if medicine.quantity < quantity:
            QMessageBox.critical(self, "Out of Stock", f"Only {medicine.quantity} in stock.")
            return

        customer_name = self.customer_name_input.text().strip()
        customer_phone = self.customer_phone_input.text().strip()

        if not customer_name or not customer_phone:
            QMessageBox.warning(self, "Missing Info", "Please enter customer name and phone.")
            return

        customer = session.query(Customer).filter_by(phone=customer_phone).first()
        if not customer:
            customer = Customer(name=customer_name, phone=customer_phone)
            session.add(customer)
            session.commit()

        total_price = medicine.price * quantity
        sale = Sale(
            customer_id=customer.id,
            medicine_id=medicine.id,
            quantity=quantity,
            total_price=total_price,
            timestamp=datetime.now()
        )
        session.add(sale)

        medicine.quantity -= quantity
        session.commit()
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sold {quantity}x {medicine.name} to {customer.name} ({customer.phone}) for ${total_price:.2f}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)

        self.load_medicines()
        QMessageBox.information(self, "Success", f"Sold {quantity}x {medicine.name} to {customer.name}.")

    def go_back_to_login(self):
        from .login_window import LoginWindow  
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

