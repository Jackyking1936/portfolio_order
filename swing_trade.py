from login_gui import LoginForm

import sys

from fubon_neo.sdk import FubonSDK
from PySide6.QtWidgets import QApplication, QWidget

from PySide6.QtGui import QIcon

class MainApp(QWidget):
    def __init__(self, active_account):
        super().__init__()

        self.active_account = active_account

        my_icon = QIcon()
        my_icon.addFile('swing.png')
        self.setWindowIcon(my_icon)
        self.setWindowTitle("Python波段單下單機")
        self.resize(1200, 600)
        

if __name__ == "__main__":
    try:
        sdk = FubonSDK()
    except ValueError:
        raise ValueError("請確認網路連線")
    active_account = None
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setStyleSheet("QWidget{font-size: 12pt;}")
    form = LoginForm(MainApp, sdk, 'swing.png')
    form.show()
    
    sys.exit(app.exec())