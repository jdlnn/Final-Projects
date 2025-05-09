from datetime import datetime
import csv

class ReminderAppMan:
    def __init__(self, data: str):
        """
        Format the reminder manager by saving the result of the reminders entered from a file
        """
        self.data = data #Storing the file name
        self.reminders = self.reminder_result() #Show result from the csv

    def reminder_result(self):
        """
        Show the result of the reminders from the csv file.
        Then if the file doesn't exist, it would return an empty list.
        """
        reminders = []
        try:
            with open(self.data, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    reminders.append({"Text": row['Text'], "Time": row['Time']})
        except FileNotFoundError:
            #Start a new empty list if the file does not exist yet.
            return []
        return reminders


    def adding_reminder(self, text: str, time: str) -> None:
        """
        This will add a new reminder to the list of reminders.
        """
        new_reminder = {"Text": text, "Time": time}
        self.reminders.append(new_reminder)

    def get_reminders(self) -> list:
        """
        This will return all the reminders
        """
        return self.reminders