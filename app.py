# main.py
import sys
from PyQt6.QtWidgets import QApplication
from appscreen import CANAnalyzerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CANAnalyzerGUI()
    window.show()
    window.setStyleSheet("background-color: #d1d1e0;")
    sys.exit(app.exec())