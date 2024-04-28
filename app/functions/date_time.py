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
