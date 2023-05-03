import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QAction
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the size and title of the main window
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("AUTO-WT TOOL")

        # Set a modern font and color scheme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2f2f2;
            }
            QLabel {
                font: 14pt "Segoe UI";
                color: #555;
            }
            QLineEdit {
                font: 14pt "Segoe UI";
                color: #555;
                border: 2px solid #bbb;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox {
                font: 14pt "Segoe UI";
                color: #555;
                border: 2px solid #bbb;
                border-radius: 5px;
                padding: 5px;
            }
            QTextEdit {
                font: 14pt "Segoe UI";
                color: #555;
                border: 2px solid #bbb;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                font: 14pt "Segoe UI";
                color: #fff;
                background-color: #0078d7;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004d88;
            }
        """)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a label widget for the URL input field
        url_label = QLabel("Enter website URL:")
        url_label.setFont(QFont("Segoe UI", 18))
        layout.addWidget(url_label)

        # Create a text input field widget for the URL
        self.url_input = QLineEdit()
        self.url_input.setFont(QFont("Segoe UI", 18))
        layout.addWidget(self.url_input)

        # Create a label widget for the SQL injection type input field
        type_label = QLabel("Select SQL injection type:")
        type_label.setFont(QFont("Segoe UI", 18))
        layout.addWidget(type_label)

        # Create a combo box widget for selecting the SQL injection type
        self.type_input = QComboBox()
        self.type_input.addItem("Union-based SQLi")
        self.type_input.addItem("Time-based SQLi")
        self.type_input.addItem("Error-based SQLi")
        self.type_input.addItem("Boolean-based SQLi")
        self.type_input.addItem("Blind-based SQLi")
        self.type_input.addItem("Content-based Blind SQLi")
        self.type_input.setFont(QFont("Segoe UI", 18))
        layout.addWidget(self.type_input)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create a button widget to initiate the testing process
        self.test_button = QPushButton(QIcon("test.png"),"Test")
        self.test_button.clicked.connect(self.run_test)
        button_layout.addWidget(self.test_button)

        # Create a button widget to clear the results area
        clear_button = QPushButton(QIcon("clear.png"), "Clear")
        clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Create a label widget for the results area
        results_label = QLabel("Results:")
        results_label.setFont(QFont("Segoe UI", 18))
        layout.addWidget(results_label)

        # Create a text edit widget for displaying the results
        self.results_text = QTextEdit()
        self.results_text.setFont(QFont("Segoe UI", 14))
        layout.addWidget(self.results_text)

        # Create a menu bar
        menubar = self.menuBar()

        # Create a File menu and add it to the menu bar
        file_menu = menubar.addMenu("File")

        # Create an Exit action and add it to the File menu
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)



    def run_test(self):
        # Implement the logic for running the SQL injection test here
        pass

    def clear_results(self):
        self.results_text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
