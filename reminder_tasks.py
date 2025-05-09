from datetime import datetime

def task(date_as_str: str) -> bool:
    try:
        datetime.strptime(date_as_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False

