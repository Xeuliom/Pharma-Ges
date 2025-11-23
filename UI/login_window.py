# ui/login_window.py
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.db_setup import User
from .admin_window import DashboardWindow

engine = create_engine('sqlite:///pharmacy.db')
Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacy Login")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.handle_login)

        layout.addWidget(QLabel("Login to Pharmacy System"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            QMessageBox.information(self, "Success", f"Welcome {user.username}!")
            self.open_dashboard(user.username)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password")

    def open_dashboard(self, username):
        self.dashboard = DashboardWindow(username)
        self.dashboard.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
