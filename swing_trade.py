from login_gui import LoginForm

import sys
from fubon_neo.sdk import FubonSDK

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QPlainTextEdit
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtCore import Qt

class MainApp(QWidget):
    def __init__(self, active_account):
        super().__init__()

        self.active_account = active_account

        my_icon = QIcon()
        my_icon.addFile('swing.png')
        self.setWindowIcon(my_icon)
        self.setWindowTitle("Python波段單下單機")
        self.resize(1200, 600)

                # 製作上下排列layout上為庫存表，下為log資訊
        layout = QVBoxLayout()

        layout_table = QHBoxLayout()
        # 庫存表表頭
        self.old_cur_header = ['股票名稱', '股票代號', '類別', '庫存股數', '庫存均價', '現價', '停損', '停利', '損益試算', '獲利率%']
        self.new_pos_header = ['股票名稱', '股票代號', '類別', '庫存股數', '庫存均價', '現價', '停損', '停利', '損益試算', '獲利率%']
        
        self.old_cur_table = QTableWidget(0, len(self.old_cur_header))
        self.old_cur_table.setHorizontalHeaderLabels([f'{item}' for item in self.old_cur_header])

        self.new_pos_table = QTableWidget(0, len(self.new_pos_header))
        self.new_pos_table.setHorizontalHeaderLabels([f'{item}' for item in self.new_pos_header])

        layout_table.addWidget(self.old_cur_table)
        layout_table.addWidget(self.new_pos_table)
        
        # 整個設定區layout
        layout_condition = QGridLayout()

        # 監控區layout設定
        label_monitor = QLabel('預設新部位停損停利設定')
        label_monitor.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; }")
        label_monitor.setAlignment(Qt.AlignCenter)
        layout_condition.addWidget(label_monitor, 0, 0)
        label_sl = QLabel('\t預設停損(%, 0為不預設停損):')
        layout_condition.addWidget(label_sl, 1, 0)
        self.lineEdit_default_sl = QLineEdit()
        self.lineEdit_default_sl.setText('-5')
        layout_condition.addWidget(self.lineEdit_default_sl, 1, 1)
        label_sl_post = QLabel('%')
        layout_condition.addWidget(label_sl_post, 1, 2)
        label_tp = QLabel('\t預設停利(%, 0為不預設停損):')
        layout_condition.addWidget(label_tp, 2, 0)
        self.lineEdit_default_tp = QLineEdit()
        self.lineEdit_default_tp.setText('5')
        layout_condition.addWidget(self.lineEdit_default_tp, 2, 1)
        label_tp_post = QLabel('%')
        layout_condition.addWidget(label_tp_post, 2, 2)

        # 啟動按鈕
        self.button_start = QPushButton('開始監控')
        self.button_start.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.button_start.setStyleSheet("QPushButton { font-size: 24px; font-weight: bold; }")
        layout_condition.addWidget(self.button_start, 0, 6, 3, 1)

        # 停止按鈕
        self.button_stop = QPushButton('停止監控')
        self.button_stop.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.button_stop.setStyleSheet("QPushButton { font-size: 24px; font-weight: bold; }")
        layout_condition.addWidget(self.button_stop, 0, 6, 3, 1)
        self.button_stop.setVisible(False)

        # 模擬區layout設定
        self.button_fake_buy_filled = QPushButton('fake buy filled')
        self.button_fake_sell_filled = QPushButton('fake sell filled')
        self.button_fake_websocket = QPushButton('fake websocket')

        layout_sim = QGridLayout()
        label_sim = QLabel('測試用按鈕')
        label_sim.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; }")
        label_sim.setAlignment(Qt.AlignCenter)
        layout_sim.addWidget(label_sim, 0, 1)
        layout_sim.addWidget(self.button_fake_buy_filled, 1, 0)
        layout_sim.addWidget(self.button_fake_sell_filled, 1, 1)
        layout_sim.addWidget(self.button_fake_websocket, 1, 2)
        
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)

        layout.addLayout(layout_table)
        layout.addLayout(layout_condition)
        layout.addLayout(layout_sim)
        layout.addWidget(self.log_text)

        layout.setStretchFactor(layout_table, 6)
        layout.setStretchFactor(layout_condition, 2)
        layout.setStretchFactor(layout_sim, 1)
        layout.setStretchFactor(self.log_text, 3)

        self.setLayout(layout)

        self.print_log("login success, 現在使用帳號: {}".format(self.active_account.account))
        self.print_log("建立行情連線...")
        sdk.init_realtime() # 建立行情連線
        self.print_log("行情連線建立OK")
        self.reststock = sdk.marketdata.rest_client.stock
        self.wsstock = sdk.marketdata.websocket_client.stock
        

    # 更新最新log到QPlainTextEdit的slot function
    def print_log(self, log_info):
        self.log_text.appendPlainText(log_info)
        self.log_text.moveCursor(QTextCursor.End)

if __name__ == "__main__":
    try:
        sdk = FubonSDK()
    except ValueError:
        raise ValueError("請確認網路連線")
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setStyleSheet("QWidget{font-size: 12pt;}")
    form = LoginForm(MainApp, sdk, 'swing.png')
    form.show()
    
    sys.exit(app.exec())