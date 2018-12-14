import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit
import binascii


class MyTextEdit(QPlainTextEdit):

    def _init_(self):

        super(MyTextEdit, self)._init_(parent)

        self.is_first_input = True

    def mousePressEvent(self, event):

        if self.is_first_input:
            self.selectAll()
            self.clear()
            self.is_first_input = False
        else:
            pass

        if event.button() == QtCore.Qt.LeftButton:

            self.startCursorPosition = event.pos()
            cursor = self.cursorForPosition(self.startCursorPosition)
            self.startPosition = cursor.position()


    def mouseMoveEvent(self, event):

        if event.button() == QtCore.Qt.NoButton:
            self.endCursorPosition = event.pos()
            cursor = self.cursorForPosition(self.endCursorPosition)
            position = cursor.position()
            cursor.setPosition(self.startPosition)
            cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            self.endCursorPosition = event.pos()
            cursor = self.cursorForPosition(self.endCursorPosition)
            position = cursor.position()
            cursor.setPosition(self.startPosition)
            cursor.setPosition(position, QtGui.QTextCursor.KeepAnchor)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test2.ui', self)
        self.action_3.triggered.connect(self.open_file)
        self.action_3.setShortcut("Ctrl+F")
        self.action_3.setStatusTip('Открытие выбранного файла')
        self.initUI()


    def initUI(self):
        self.hex_text = MyTextEdit(self)
        self.hex_text.move(0,50)
        self.hex_text.resize(500, 500)
        self.common_text = MyTextEdit(self)
        self.common_text.move(550, 50)
        self.common_text.resize(200, 500)





    def open_file(self):
        global hexdata
        global read_data
        global splited_hex
        file_path = QFileDialog.getOpenFileName(self)
        with open(file_path[0], mode= "rb") as f:
             read_data = f.read()
             f.close()
        hexdata = read_data.hex()
        splited_hex = ' '.join([hexdata[i:i + 2] for i in range(0, len(hexdata), 2)])
        self.hex_text.setPlainText(splited_hex)
        b = bytes.fromhex(hexdata)
        self.common_text.setPlainText(b.decode("utf8"))




app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
