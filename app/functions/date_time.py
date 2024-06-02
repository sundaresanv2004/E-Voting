from datetime import datetime, date
import calendar

now = datetime.now()
hour = now.hour

if hour < 12:
    current_time = "Good Morning"
elif hour < 16:
    current_time = "Good Afternoon"
else:
    current_time = "Good Evening"

present_date = date.today()
present_year = present_date.year
present_month = present_date.month
present_day = present_date.day
months_ = list(calendar.month_name)[1:]

if present_month >= 6:
    current_academic_year = f'{present_year}-{present_year + 1}'
else:
    current_academic_year = f'{present_year - 1}-{present_year}'
