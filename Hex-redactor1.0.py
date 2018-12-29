import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit
from PyQt5.QtWidgets import QColorDialog, QInputDialog, QFontDialog
import binascii


class MyTextEdit(QPlainTextEdit):
    is_first_input = True

    def __init__(self, parent):
        super(MyTextEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        if self.is_first_input:
            self.selectAll()
            # self.clear()
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


def transform_plain_text_to_hex(plain_text):
    b = plain_text.encode('utf-8')
    hexdata = b.hex()
    return ' '.join([hexdata[i:i + 2] for i in range(0, len(hexdata), 2)])


def transform_hex_text_to_plain(hex_text):
    b_text = ''.join(hex_text.split())
    b = bytes.fromhex(b_text)
    return b.decode('utf-8')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_text_inserted = False
        uic.loadUi('Window_design.ui', self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def initUI(self):
        self.action_3.triggered.connect(self.open_file)
        self.action_3.setShortcut("Ctrl+O")
        self.action_3.setStatusTip('Открытие выбранного файла')

        self.action_4.triggered.connect(self.save_file)
        self.action_4.setShortcut("Ctrl+S")
        self.action_4.setStatusTip('Сохранение файла')

        self.action_2.triggered.connect(self.change_background)
        self.action_2.setShortcut("Alt+F")
        self.action_2.setStatusTip('Изменение цвета текстового поля')

        self.action_5.triggered.connect(self.change_font_and_size)
        self.action_5.setShortcut("Alt+R")
        self.action_5.setStatusTip('Изменение шрифта')


        self.plain_text_field = MyTextEdit(self)
        self.plain_text_field.move(20, 52)
        self.plain_text_field.resize(200, 500)
        self.plain_text_field.textChanged.connect(self.plain_text_input)


        self.hex_text_field = MyTextEdit(self)
        self.hex_text_field.move(250, 52)
        self.hex_text_field.resize(500, 500)
        self.hex_text_field.textChanged.connect(self.hex_text_input)

    def change_background(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.hex_text_field.setStyleSheet(
                "background-color: {}".format(color.name())
            )
        if color.isValid():
            self.plain_text_field.setStyleSheet(
                "background-color: {}".format(color.name())
            )

    def change_font_and_size(self):
        try:
            font, ok = QFontDialog.getFont()
            if ok:
                self.hex_text_field.setFont(font)
                self.plain_text_field.setFont(font)

        except:
            pass

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self)
        if file_path[0] == '':
            pass
        else:
            with open(file_path[0], mode="rb") as f:
                read_data = f.read()
                f.close()
            hexdata = read_data.hex()
            splited_hex = ' '.join([hexdata[i:i + 2] for i in range(0, len(hexdata), 2)])
            self.hex_text_field.setPlainText(splited_hex)
            b = bytes.fromhex(hexdata)
            self.plain_text_field.setPlainText(b.decode("utf8"))

    def save_file(self):
        file_path = QFileDialog.getSaveFileName(self)
        if file_path[0] == '':
            pass
        else:
            with open(file_path[0], mode="rb") as f:
                read_data = f.read()
                f.close()

    def get_hex_bytes(self):
        b_text = ''.join(self.hex_text_field.toPlainText().split())
        b = bytes.fromhex(b_text)
        return b

    def hex_text_input(self):
        if self.is_text_inserted:
            pass

        try:
            plain_text = transform_hex_text_to_plain(self.hex_text_field.toPlainText())
            self.is_text_inserted = True
            if plain_text != self.plain_text_field.toPlainText():
                self.plain_text_field.setPlainText(plain_text)
                self.is_text_inserted = False
        except:
            pass

    def plain_text_input(self):
        if self.is_text_inserted:
            pass

        hex_text = transform_plain_text_to_hex(self.plain_text_field.toPlainText())
        self.is_text_inserted = True
        self.hex_text_field.setPlainText(hex_text)
        self.is_text_inserted = False


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())