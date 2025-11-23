# ui/welcome_window.py
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from .login_window import LoginWindow
from .user_window import UserWindow

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacy App")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to Pharmacy System"))

        self.admin_button = QPushButton("Admin")
        self.admin_button.clicked.connect(self.open_admin_dialog)
        layout.addWidget(self.admin_button)

        self.user_button = QPushButton("User")
        self.user_button.clicked.connect(self.open_user_dialog)
        layout.addWidget(self.user_button)

        self.setLayout(layout)

    def open_user_dialog(self):
        self.user_window = UserWindow()
        self.user_window.show()
        self.close()

    def open_admin_dialog(self):
        self.admin_window = LoginWindow()
        self.admin_window.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec())
