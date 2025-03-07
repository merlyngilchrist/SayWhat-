from PyQt6.QtWidgets import QApplication, QLabel, QWidget
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("SayWhat? - Test")
label = QLabel("Hellow, SayWhat!", parent=window)
window.show()
sys.exit(app.exec())