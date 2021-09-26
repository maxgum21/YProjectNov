from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QDialog, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic
import MusCompiler


class SB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("SB.ui", self)
        self.state = 'n'
        self.r_normal.toggle()
        self.default = True
        self.b_list = [
            self.b1, self.b2, self.b3, self.b4,
            self.b5, self.b6, self.b7, self.b8,
            self.b9, self.b10, self.b11, self.b12,
            self.b13, self.b14, self.b15, self.b16
        ]

        self.b_list2 = [
            Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
            Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R,
            Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F,
            Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_V
        ]

        self.qbl = [self.b1, self.b2, self.b3, self.b4,
                    self.b5, self.b6, self.b7, self.b8,
                    self.b9, self.b10, self.b11, self.b12,
                    self.b13, self.b14, self.b15, self.b16
                    ]

        self.changing = False
        self.ui()

    def ui(self):
        self.setWindowIcon(QIcon('WindowIcon.jpg'))
        for i in range(len(self.b_list)):
            self.b_list[i].clicked.connect(self.soundit)

        self.add.clicked.connect(self.ch)
        self.defaultB.clicked.connect(self.createWarn)
        self.manual.clicked.connect(self.createManual)

        self.buttonGroup.buttonClicked.connect(self.setState)
        for i in range(16):
            self.qbl[i].setStyleSheet(f"background-image : url(KeyImgs/Key{i + 1}.jpg);")

        self.add.setStyleSheet("background-image : url(KeyAdd.jpg);")
        self.defaultB.setStyleSheet("background-image : url(KeyDefault.jpg);")
        self.manual.setStyleSheet("background-image : url(KeyManual.jpg);")

    def keyPressEvent(self, event):
        if event.key() in self.b_list2:
            n = self.b_list2.index(event.key())
            self.soundit(n, True)
        elif event.key() == Qt.Key_Shift:
            if self.state == 'r':
                self.r_normal.toggle()
                self.state = 'n'
            elif self.state == 'n':
                self.r_reverse.toggle()
                self.state = 'r'

    def soundit(self, n, kb=False):
        if kb:
            if self.state == 'n':
                # self.qbl[n].setStyleSheet(f"background-image : url(KeyImgsP/KeyP{n + 1}.jpg);")
                MusCompiler.musPlayer(n + 1)
                # self.qbl[n].setStyleSheet(f"background-image : url(KeyImgs/Key{n + 1}.jpg);")
            elif self.state == 'r':
                # self.qbl[n].setStyleSheet(f"background-image : url(KeyImgsP/KeyP{n + 1}.jpg);")
                MusCompiler.musPlayer_r(n + 1)
                # self.qbl[n].setStyleSheet(f"background-image : url(KeyImgs/Key{n + 1}.jpg);")
        else:
            if not self.changing:
                n = self.b_list.index(self.sender()) + 1
                if self.state == 'n':
                    #     self.qbl[n - 1].setStyleSheet(f"background-image : url(KeyImgsP/KeyP{n}.jpg);")
                    MusCompiler.musPlayer(n)
                    #     self.qbl[n - 1].setStyleSheet(f"background-image : url(KeyImgs/Key{n}.jpg);")
                elif self.state == 'r':
                    # self.qbl[n - 1].setStyleSheet(f"background-image : url(KeyImgsP/KeyP{n}.jpg);")
                    MusCompiler.musPlayer_r(self.b_list.index(self.sender()) + 1)
                    # self.qbl[n - 1].setStyleSheet(f"background-image : url(KeyImgs/Key{n}.jpg);")
            else:
                fname = QFileDialog.getOpenFileName(self, 'Выберите Файл', '', '*.wav')[0]
                MusCompiler.musChanger(self.b_list.index(self.sender()) + 1, fname)
                self.default = False
                self.ch()

    def ch(self):
        self.changing = not self.changing
        if self.changing:
            self.add.setStyleSheet("background-image : url(KeyAddPressed.jpg);")
        else:
            self.add.setStyleSheet("background-image : url(KeyAdd.jpg);")

    def set_default(self):
        MusCompiler.musReset()
        self.default = True

    def setState(self, button):
        if button == self.r_normal:
            self.state = 'n'
        elif button == self.r_reverse:
            self.state = 'r'

    def createWarn(self):
        if not self.default:
            self.dialog = DialogWarn(self)
            self.dialog.show()

    def createManual(self):
        self.dialog = DialogManual(self)
        self.dialog.show()


class DialogWarn(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        x, y = self.parent.x() + 150, self.parent.y() + 150
        self.setGeometry(x, y, 650, 100)
        self.setWindowTitle('Внимание!')
        self.setModal(True)
        self.setWindowIcon(QIcon("WarnIcon.jpg"))

        msg = '''Если вы вернете начальные звуки все сохраненые вами звуки будут недоступны
                Вы уверены что вы хотите вернуть звуки по умолчанию?'''
        self.l = QLabel(msg, self)
        font = QFont('MS Shell Dlg 2', pointSize=9)
        font.setBold(True)
        self.l.setFont(font)
        self.l.setGeometry(10, 0, 650, 70)
        self.ok_button = QPushButton('OK', self)
        self.cancel_button = QPushButton('Отменить', self)
        self.ok_button.setGeometry(180, 58, 100, 35)
        self.cancel_button.setGeometry(380, 58, 100, 35)

        self.ok_button.clicked.connect(self.ok)
        self.cancel_button.clicked.connect(self.cancel)

    def ok(self):
        self.parent.output = True
        self.close()

    def cancel(self):
        self.parent.output = False
        self.parent.close()

    def closeEvent(self, event):
        if self.parent.output:
            self.parent.set_default()


class DialogManual(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        x, y = self.parent.x() + 100, self.parent.y() + 100
        self.setGeometry(x, y, 700, 300)
        self.setWindowTitle('Инструкция')
        self.setModal(True)
        self.setWindowIcon(QIcon("Manual_Icon.jpg"))
        msg = '''Это Инструкция созданая для того, чтобы помочь вам с данным приложением.
        
        Для включения звуков вы можете нажать мышкой на кнопки на экране,
        или нажать на клавишу на вашей клавиатуре соответствующую кнопке на экране.
        
        Для переключения режима звуков, с Нормального на Реверс, или наоборот,
        нажмите на клавишу Shift, или выберете режим мышкой на экране.
        
        Также вы можете добавить ваши звуки (только в формате .wav),
        или вернуть их на стандартные
        (только если вы уже поменяли звуки).'''
        self.l = QLabel(msg, self)
        font = QFont('MS Shell Dlg 2', pointSize=9)
        font.setBold(True)
        self.l.setFont(font)
        self.l.setGeometry(10, -80, 690, 400)
        self.close_button = QPushButton('Закрыть', self)
        self.close_button.setGeometry(400, 255, 75, 30)
        self.close_button.clicked.connect(self.closeit)

    def closeit(self):
        self.close()