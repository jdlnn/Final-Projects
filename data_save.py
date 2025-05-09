import csv

def data_saved(data: str, reminders: list) -> None:
    """
    This function will save the reminders in the csv file.
    :param data: The name of the csv file
    :param reminders: The list of reminder to save
    """

    with open(data, 'w', newline='') as file:
        fieldnames = ["Text", "Time"] #Text and Time are the csv headers
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() # This where it write the header row of text, time
        #This writes each reminder into the csv using dictionary
        for reminder in reminders:
            writer.writerow(reminder)
