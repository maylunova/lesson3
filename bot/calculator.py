'''
Бот-калкулятор

Научите бота выполнять основные арифметические действия с числами: сложение, вычитание, умножение и деление. 
Если боту сказать “2-3=”, он должен ответить “-1”. Все выражения для калькулятора должны заканчиваться знаком равно.
Дополнительно: не забудьте обработать возможные ошибки во вводе: пробелы, отсутствие чисел, деление на ноль.
'''

import re

import common

PATTERN = re.compile(r'\s*(\d*\.{0,1}\d*)\s*([+\-*\/])\s*(\d*\.{0,1}\d*)\s*[=]{0,1}\s*')

def calculate(bot, update, user_data):
    user_text = update.message.text
    match = PATTERN.match(user_text)
    
    if match is None:
        update.message.reply_text('Incorrect input!' + '\n\n' + common.GREETING)
        return
    
    groups = match.groups()
    first_num_str = groups[0]
    second_num_str = groups[2]

    if len(first_num_str) == 0 or len(second_num_str) == 0:
        update.message.reply_text('Incorrect input!' + '\n\n' + common.GREETING)
        return

    first_num = float(first_num_str)
    second_num = float(second_num_str)
    action = groups[1]

    if action == '+':
        update.message.reply_text(str(first_num + second_num) + '\n\n' + common.GREETING)
    if action == '-':
        update.message.reply_text(str(first_num - second_num) + '\n\n' + common.GREETING)
    if action == '*':
        update.message.reply_text(str(first_num * second_num) + '\n\n' + common.GREETING)
    if action == '/':
        try:
            update.message.reply_text(str(first_num / second_num) + '\n\n' + common.GREETING)
        except ZeroDivisionError:
            update.message.reply_text('Division by zero!' + '\n\n' + common.GREETING)