# ui/add_edit_medicine.py
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDateEdit, QVBoxLayout
)
from PySide6.QtCore import QDate
from core import inventory_manager
from datetime import datetime

class AddEditMedicineDialog(QDialog):
    def __init__(self, parent=None, medicine=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Medicine")
        self.setMinimumWidth(300)
        self.medicine = medicine

        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.price_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.expiry_input = QDateEdit()
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDate(QDate.currentDate())

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Expiry Date:", self.expiry_input)

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.save_data)
        self.cancel_button.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        if self.medicine:
            self.load_medicine_data()

    def load_medicine_data(self):
        self.name_input.setText(self.medicine.name)
        self.category_input.setText(self.medicine.category)
        self.price_input.setText(str(self.medicine.price))
        self.quantity_input.setText(str(self.medicine.quantity))
        if self.medicine.expiry_date:
            self.expiry_input.setDate(QDate.fromString(self.medicine.expiry_date.strftime('%Y-%m-%d'), 'yyyy-MM-dd'))

    def save_data(self):
        try:
            name = self.name_input.text()
            category = self.category_input.text()
            price = float(self.price_input.text())
            quantity = int(self.quantity_input.text())
            expiry_date = self.expiry_input.date().toPython()

            if self.medicine:
                inventory_manager.update_medicine(
                    self.medicine.id, name, category, price, quantity, expiry_date
                )
            else:
                inventory_manager.add_medicine(
                    name, category, price, quantity, expiry_date
                )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save medicine: {e}")
