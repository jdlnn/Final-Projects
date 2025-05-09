from PyQt6.QtWidgets import QApplication, QMainWindow
from voting_gui import Ui_MainWindow
from voting_pyqt6 import Voting
def main():
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window = Voting()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
