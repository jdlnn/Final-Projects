import tkinter as tk
from tkinter import messagebox, Tk
from reminder import ReminderAppMan
from reminder_tasks import task
from data_save import data_saved

class Reminder:
    def __init__(self, root):
        self.root = root #Main window
        self.root.title("Reminder") #Window title
        self.root.geometry("400x300") #Window size

        self.reminder_man = ReminderAppMan('reminder.csv')
        self.reminder_frame = None
        #Display a label saying, "Add New Reminder"
        self.reminder_label = tk.Label(root, text="Add New Reminder")
        self.reminder_label.pack()

        #Display an entry box where user can type the reminder
        self.reminder_entry = tk.Entry(root, width=40)
        self.reminder_entry.pack()

        #Display a label for the date/time
        self.date_label = tk.Label(root, text='Enter Reminder Date (MM/DD/YYYY)')
        self.date_label.pack()

        #Display an entry box where user can type the date
        self.date_entry = tk.Entry(root, width=40)
        self.date_entry.pack()

        #
        self.time_variable = tk.StringVar(value='Time')
        self.time_menu = tk.OptionMenu(root, self.time_variable, *[
            '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00',
            '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30',
            '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00',
            '11:30', '12:00', '12:30'
        ])
        self.time_menu.pack()

        #RadioButton for AM and PM for the time
        self.ampm_variable = tk.StringVar(value=' ')
        ampm_frame = tk.Frame(root)
        ampm_frame.pack()

        self.am_radio = tk.Radiobutton(ampm_frame, text='AM', variable=self.ampm_variable, value='AM')
        self.am_radio.pack(side='left',padx=10)

        self.pm_radio = tk.Radiobutton(ampm_frame, text='PM', variable=self.ampm_variable, value='PM')
        self.pm_radio.pack(side='left',padx=10)

        #Display a button where the user save its reminder
        self.new_button = tk.Button(root, text='Submit Reminder', command=self.new_reminder)
        self.new_button.pack()

        #Display a button to view all the reminder of the user
        self.view_button = tk.Button(root, text='View Reminders', command=self.view_reminders)
        self.view_button.pack()

        self.message_label = tk.Label(root, text='',fg='red')
        self.message_label.pack(pady=10)

    def new_reminder(self):
        """
        Add new reminder
        """
        reminder_text = self.reminder_entry.get()
        date_text = self.date_entry.get()
        time = self.time_variable.get()
        ampm = self.ampm_variable.get()

        self.message_label.config(text=' ')
        #This check if any info are missing
        if not reminder_text or time == 'Time' or ampm not in ('AM', 'PM'):
            self.message_label.config(text='Please fill out the fields.',fg='red')
            return
        # Check if date is valid
        if not task(date_text):
            # This shows an invalid message if the date is invalid
            self.message_label.config(text="Invalid reminder date. Please enter as (MM/DD/YYYY)",fg='red')
            return

        # This combines the output
        ampm_time = f'{date_text}, {time} {ampm}'

        for reminder in self.reminder_man.get_reminders():
            if reminder['Time'] == ampm_time:
                self.message_label.config(text='This date and time is already exists',fg='red')
                return

        # This is where it let the user know that the reminder is added
        self.message_label.config(text="Reminder added", fg='green')
        #This is where it save the reminder
        self.reminder_man.adding_reminder(reminder_text, ampm_time)
        data_saved('reminder.csv', self.reminder_man.get_reminders())


        #This deletes the entries after it get saved
        self.reminder_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_variable.set('Time')
        self.ampm_variable.set(' ')

    def view_reminders(self):
        """
        This will display the saved reminders in a message box and the deleted reminders button
        """
        #This will destroy old frame reminder so it wouldn't overlap/crashed
        if self.reminder_frame is not None:
            self.reminder_frame.destroy()
        self.root.geometry("400x600")

        #This creates a new frame showing all of the reminders and gets the reminder
        self.reminder_frame = tk.Frame(self.root, bg='lightgrey')
        self.reminder_frame.pack(side='right', fill='both',expand=True)
        reminders = self.reminder_man.get_reminders()

        #This shows the message if there is no reminder
        if not reminders:
            tk.Label(self.reminder_frame, text="No reminders added yet",bg='lightgrey').pack(pady=20)
        else:
            #Your Reminders label
            tk.Label(self.reminder_frame, text="Your Reminders", bg='lightgrey').pack(pady=20)
            #This organizes the reminders in rows
            org_frame = tk.Frame(self.reminder_frame, bg='lightgrey')
            org_frame.pack(fill='both', expand=True)

        #This is to organize the reminders
        for i, reminder in enumerate(reminders):
            reminder_text = reminder['Text']
            reminder_time = reminder['Time']

            reminder_row = tk.Frame(self.reminder_frame, bg='lightgrey')
            reminder_row.pack(fill='x', pady=5)
            #Label for the text
            reminder_label = tk.Label(reminder_row, text=f'{reminder_text} at {reminder_time}', bg='lightgrey')
            reminder_label.pack(side='left', pady=10)
            #Delete button if the user want to delete their reminder
            delete_button = tk.Button(reminder_row, text='Delete Reminder', command=self.create_delete_handler(i))
            delete_button.pack(side='right',padx=10,pady=10)
        #This is a close button to close the view reminder
        close_button = tk.Button(self.reminder_frame, text='Close', command=self.close_frame)
        close_button.pack(side='right',anchor='ne',pady=10,padx=10)

    def create_delete_handler(self, i: int):
        """
        This function is where the delete button handler for each reminder
        """
        def delete_reminder():
            del self.reminder_man.reminders[i]
            data_saved('reminder.csv', self.reminder_man.get_reminders())
            self.view_reminders()
        return delete_reminder
    def close_frame(self):
        """
        This function will close the frame from view reminders when the user clicked close,
        then it reset the main window size.
        """
        if self.reminder_frame is not None:
            self.reminder_frame.destroy()
            self.reminder_frame = None
            self.root.geometry("400x300")
def main() -> None:
    root = tk.Tk()
    app = Reminder(root)
    root.mainloop()


if __name__ == '__main__':
    main()

