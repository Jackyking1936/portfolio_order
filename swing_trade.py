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
        self.old_cur_header = ['股票名稱', '股票代號', '類別', '庫存股數', '庫存均價', '現價', '損益試算', '獲利率%']
        self.new_pos_header = ['股票名稱', '股票代號', '現價', '委託數量', '委託價格', '成交數量', '成交價格']
        
        self.old_cur_table = QTableWidget(0, len(self.old_cur_header))
        self.old_cur_table.setHorizontalHeaderLabels([f'{item}' for item in self.old_cur_header])

        self.new_pos_table = QTableWidget(0, len(self.new_pos_header))
        self.new_pos_table.setHorizontalHeaderLabels([f'{item}' for item in self.new_pos_header])

        layout_table.addWidget(self.old_cur_table)
        layout_table.addWidget(self.new_pos_table)
        
        # 整個設定區layout
        layout_parameter = QGridLayout()

        # 參數設置區layout設定
        label_input_title = QLabel('配置參數設定')
        label_input_title.setStyleSheet("QLabel { font-size: 24px; font-weight: bold; }")
        label_input_title.setAlignment(Qt.AlignCenter)
        layout_parameter.addWidget(label_input_title, 0, 0)

        label_total_amount = QLabel('配置總金額:')
        layout_parameter.addWidget(label_total_amount, 1, 0)
        label_total_amount.setAlignment(Qt.AlignRight)
        self.lineEdit_default_total_amount = QLineEdit()
        self.lineEdit_default_total_amount.setText('100')
        layout_parameter.addWidget(self.lineEdit_default_total_amount, 1, 1)
        label_total_amount_post = QLabel('萬元, ')
        layout_parameter.addWidget(label_total_amount_post, 1, 2)

        label_file_path = QLabel('目標清單路徑:')
        layout_parameter.addWidget(label_file_path, 0, 3)
        self.lineEdit_default_file_path = QLineEdit()
        layout_parameter.addWidget(self.lineEdit_default_file_path, 0, 4)
        folder_btn = QPushButton('')
        folder_btn.setIcon(QIcon('folder.png'))
        layout_parameter.addWidget(folder_btn, 0, 5)

        label_est_sell = QLabel('預估賣出金額:')
        layout_parameter.addWidget(label_est_sell, 1, 3)
        self.lineEdit_default_est_sell = QLineEdit()
        self.lineEdit_default_est_sell.setReadOnly(True)
        layout_parameter.addWidget(self.lineEdit_default_est_sell, 1, 4)
        label_est_sell_post = QLabel('元')
        layout_parameter.addWidget(label_est_sell_post, 1, 5)

        label_est_buy = QLabel('預估買進金額:')
        layout_parameter.addWidget(label_est_buy, 2, 3)
        self.lineEdit_default_est_buy = QLineEdit()
        self.lineEdit_default_est_buy.setReadOnly(True)
        layout_parameter.addWidget(self.lineEdit_default_est_buy, 2, 4)
        label_est_buy_post = QLabel('元')
        layout_parameter.addWidget(label_est_buy_post, 2, 5)

        label_est_pnl = QLabel('預估賣出損益:')
        layout_parameter.addWidget(label_est_pnl, 3, 3)
        self.lineEdit_default_est_pnl = QLineEdit()
        self.lineEdit_default_est_pnl.setReadOnly(True)
        layout_parameter.addWidget(self.lineEdit_default_est_pnl, 3, 4)
        label_est_pnl_post = QLabel('元')
        layout_parameter.addWidget(label_est_pnl_post, 3, 5)

        # 啟動按鈕
        self.button_start = QPushButton('開始下單')
        self.button_start.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.button_start.setStyleSheet("QPushButton { font-size: 24px; font-weight: bold; }")
        layout_parameter.addWidget(self.button_start, 1, 6, 3, 1)

        # 停止按鈕
        self.button_stop = QPushButton('停止下單')
        self.button_stop.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.button_stop.setStyleSheet("QPushButton { font-size: 24px; font-weight: bold; }")
        layout_parameter.addWidget(self.button_stop, 1, 6, 3, 1)
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
        layout.addLayout(layout_parameter)
        layout.addLayout(layout_sim)
        layout.addWidget(self.log_text)

        layout.setStretchFactor(layout_table, 7)
        layout.setStretchFactor(layout_parameter, 1)
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