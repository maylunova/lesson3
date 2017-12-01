'''
Напечатайте в консоль даты: вчера, сегодня, месяц назад
Превратите строку "01/01/17 12:10:03.234567" в объект datetime
'''

from datetime import datetime, date, timedelta, time

today = datetime.now()
delta_for_yesterday = timedelta(days=1)
delta_for_mounth_ago = timedelta(days=30)
yesterday = today - delta_for_yesterday
mounth_ago = today - delta_for_mounth_ago

date_string = '01/01/17 12:10:03.234567' 
datetime_object = datetime.strptime(date_string, "%d/%m/%y %H:%M:%S.%f")

print(yesterday)
print(today)
print(mounth_ago)
print(datetime_object)
print(type(datetime_object))