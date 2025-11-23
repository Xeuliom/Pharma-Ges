import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from UI.welcome_window import WelcomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setWindowIcon(QIcon("logo.png"))
    
    window = WelcomeWindow()  
    window.show()  
    sys.exit(app.exec())
