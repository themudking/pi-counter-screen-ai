import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class CounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Counter (PyQt5)")
        self.setGeometry(100, 100, 300, 200)  # Adjust size as needed

        self.counter = 0
        self.label = QLabel("Count: 0")
        self.label.setAlignment(Qt.AlignCenter) # Center the text

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_count(self):
        self.counter += 1
        self.label.setText(f"Count: {self.counter}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    counter_app = CounterApp()
    counter_app.show()
    app.exec_()
