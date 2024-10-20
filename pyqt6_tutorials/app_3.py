import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("My App")
        
        checkbox = QCheckBox()
        checkbox.setCheckState(Qt.CheckState.Checked)
        checkbox.stateChanged.connect(self.show_state)
        
        self.setCentralWidget(checkbox)
    
    def show_state():
        print(s == Qt.CheckState.Checked.value)
        print(s)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()