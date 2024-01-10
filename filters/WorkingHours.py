from datetime import datetime

from aiogram.dispatcher.filters import BoundFilter

restaurant_working_hours = {
    'opening_time': datetime.time(10, 0),  # Replace with the actual opening time
    'closing_time': datetime.time(20, 0),  # Replace with the actual closing time
}


# class IsWorkingHours(BoundFilter)
