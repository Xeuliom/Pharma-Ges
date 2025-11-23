from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit,QHeaderView, QGroupBox, QPushButton, QHBoxLayout, QMessageBox
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database.db_setup import Medicine
from .add_edit_medicine import AddEditMedicineDialog
from .all_sales_window import AllSalesWindow


engine = create_engine('sqlite:///pharmacy.db')
Session = sessionmaker(bind=engine)
session = Session()


class DashboardWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Pharmacy Admin Dashboard")
        self.setGeometry(150, 150, 800, 500)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search medicines by name...")
        self.search_bar.textChanged.connect(self.filter_medicines)
        
        self.view_sales_button = QPushButton("View All Sales")
        self.view_sales_button.clicked.connect(self.open_all_sales)


        self.user_mode_button = QPushButton("Go to User Mode")
        self.user_mode_button.clicked.connect(self.open_user_mode)

        welcome_label = QLabel(f"Welcome, {username}!")
        welcome_label.setStyleSheet("font-size: 20px; margin: 10px;")

        self.medicine_table = QTableWidget()
        self.medicine_table.setColumnCount(6)
        self.medicine_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price", "Quantity", "Expiry"])
        self.medicine_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.medicine_table.setSelectionBehavior(QTableWidget.SelectRows)

        self.load_medicines()

        self.add_button = QPushButton("Add Medicine")
        self.add_button.clicked.connect(self.open_add_dialog)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.open_edit_dialog)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected_medicine)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.user_mode_button)
        button_layout.addWidget(self.view_sales_button)


        inventory_box = QGroupBox("Inventory")
        inventory_layout = QVBoxLayout()
        inventory_layout.addLayout(button_layout)
        inventory_layout.addWidget(self.medicine_table)
        inventory_box.setLayout(inventory_layout)

        central_widget = QWidget()
        layout = QVBoxLayout()  # Create the layout first

        layout.addWidget(welcome_label)
        layout.addWidget(self.search_bar)  # Then add the search bar
        layout.addWidget(inventory_box)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def load_medicines(self, search_text=""):
        if search_text:
            medicines = session.query(Medicine).filter(Medicine.name.ilike(f"%{search_text}%")).all()
        else:
            medicines = session.query(Medicine).all()

        self.medicine_table.setRowCount(len(medicines))
        for row, med in enumerate(medicines):
            self.medicine_table.setItem(row, 0, QTableWidgetItem(str(med.id)))
            self.medicine_table.setItem(row, 1, QTableWidgetItem(med.name))
            self.medicine_table.setItem(row, 2, QTableWidgetItem(med.category))
            self.medicine_table.setItem(row, 3, QTableWidgetItem(f"{med.price:.2f}"))
            self.medicine_table.setItem(row, 4, QTableWidgetItem(str(med.quantity)))
            self.medicine_table.setItem(row, 5, QTableWidgetItem(
                med.expiry_date.strftime("%Y-%m-%d") if med.expiry_date else ""))

    def filter_medicines(self, text):
        self.load_medicines(search_text=text)

    def open_add_dialog(self):
        dialog = AddEditMedicineDialog(self)
        if dialog.exec():
            self.load_medicines()
            
    def open_user_mode(self):
        from .user_window import UserWindow
        self.user_window = UserWindow()
        self.user_window.show()
        self.close()        

    def open_edit_dialog(self):
        selected_row = self.medicine_table.currentRow()
        if selected_row >= 0:
            med_id = int(self.medicine_table.item(selected_row, 0).text())

            # Instead of passing the old instance, pass just the ID
            # and reload it after edit
            medicine = session.query(Medicine).get(med_id)
            if medicine:
                dialog = AddEditMedicineDialog(self, medicine)
                if dialog.exec():
                    session.expire_all()  # Forces SQLAlchemy to reload all objects from DB
                    self.load_medicines()

    def delete_selected_medicine(self):
        selected_row = self.medicine_table.currentRow()
        if selected_row >= 0:
            med_id = int(self.medicine_table.item(selected_row, 0).text())
            medicine = session.query(Medicine).get(med_id)
            if medicine:
                session.delete(medicine)
                session.commit()
                self.load_medicines()
                QMessageBox.information(
                    self, "Success", "Medicine deleted successfully.")
            else:
                QMessageBox.warning(self, "Not Found",
                                    "Selected medicine not found.")
        else:
            QMessageBox.warning(self, "No Selection",
                                "Please select a medicine to delete.")
    
    def open_all_sales(self):
        self.sales_window = AllSalesWindow()
        self.sales_window.show()

