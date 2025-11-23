# all_sales_window.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
)
from database.db_setup import Sale, Medicine, Customer, get_session

session = get_session()

class AllSalesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All Sales")
        self.setGeometry(250, 250, 900, 500)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by medicine, customer name, or phone...")
        self.search_input.textChanged.connect(self.load_sales)

        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(6)
        self.sales_table.setHorizontalHeaderLabels(["Date", "Medicine", "Customer", "Phone", "Quantity", "Total Price"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sales Records"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.sales_table)

        self.setLayout(layout)
        self.load_sales()

    def load_sales(self):
        keyword = self.search_input.text().lower()
        sales = session.query(Sale).all()

        self.sales_table.setRowCount(0)
        for sale in sales:
            medicine = session.query(Medicine).get(sale.medicine_id)
            customer = session.query(Customer).get(sale.customer_id)

            # Skip if medicine or customer is missing (deleted or inconsistent DB)
            if not medicine or not customer:
                continue

            if keyword and not (
                keyword in medicine.name.lower()
                or keyword in customer.name.lower()
                or keyword in customer.phone.lower()
            ):
                continue

            row = self.sales_table.rowCount()
            self.sales_table.insertRow(row)
            self.sales_table.setItem(row, 0, QTableWidgetItem(sale.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
            self.sales_table.setItem(row, 1, QTableWidgetItem(medicine.name))
            self.sales_table.setItem(row, 2, QTableWidgetItem(customer.name))
            self.sales_table.setItem(row, 3, QTableWidgetItem(customer.phone))
            self.sales_table.setItem(row, 4, QTableWidgetItem(str(sale.quantity)))
            self.sales_table.setItem(row, 5, QTableWidgetItem(f"${sale.total_price:.2f}"))
