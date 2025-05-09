import csv
from typing import Dict
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from voting_gui import Ui_MainWindow

class Voting(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.vote = {'John': 0, 'Jane': 0}
        self.vote_results = {}

        self.submit_button.clicked.connect(self.valid_vote)

    def valid_vote(self):
        id_entered = self.lineEdit.text()
        candidate = None


        if self.john_radiobutton.isChecked():
            candidate = 'John'
        elif self.jane_radiobutton.isChecked():
            candidate = 'Jane'

        try:
            self.voted(candidate, id_entered)
            self.message_label('Vote is submitted')

            self.lineEdit.clear()
            self.john_radiobutton.setChecked(False)
            self.jane_radiobutton.setChecked(False)

        except ValueError as e:
            self.message_label(str(e))

    def voted(self, candidate: str, user_id: str) -> None:
        if not user_id.isdigit() or len(user_id) != 5 and candidate is None:
            raise ValueError('Please fill out all the fields.')
        elif candidate is None:
            raise ValueError('Please select a candidate.')

        if not user_id.isdigit() or len(user_id) != 5:
            raise ValueError('Invalid id. Please enter a 5-digit number.')



        if user_id in self.vote_results:
            raise ValueError('Already voted.')


        self.vote[candidate] += 1
        self.vote_results[user_id] = candidate
        self.saved_votes()

    def total_votes(self) -> int:
        return self.vote['John'] + self.vote['Jane']

    def get_votes(self) -> Dict[str,int]:
        return {'John': self.vote['John'], 'Jane': self.vote['Jane'], 'Total': self.total_votes()}

    def saved_votes(self) -> None:
        with open('votes.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for user_id, candidate in self.vote_results.items():
                writer.writerow([user_id, candidate, 1])
            writer.writerow(['Total', self.total_votes()])
    def message_label(self,messages: str):
        message = QMessageBox()
        message.setText(messages)
        message.exec()