import sys
from PyQt5.QtWidgets import QApplication
from sbUI import SB

mainApp = QApplication(sys.argv)

soundboard = SB()
soundboard.show()

sys.exit(mainApp.exec())