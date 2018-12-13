import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QFileDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test2.ui', self)
        self.action_3.triggered.connect(self.open_file)
        self.action_3.setShortcut("Ctrl+Q")
        self.action_3.setStatusTip('Открытие выбранного файла')

    def chunks(lst, count):
        start = 0
        for i in range(count):
            stop = start + len(lst[i::count])
            yield lst[start:stop]
            start = stop

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self)
        with open(file_path[0], mode= "rb") as f:
             read_data = f.read()
             f.close()
        a = list(read_data.hex())



        self.textEdit.setText(b)



app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
