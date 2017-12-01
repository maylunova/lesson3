'''
Бот-калкулятор

Научите бота выполнять основные арифметические действия с числами: сложение, вычитание, умножение и деление. 
Если боту сказать “2-3=”, он должен ответить “-1”. Все выражения для калькулятора должны заканчиваться знаком равно.
Дополнительно: не забудьте обработать возможные ошибки во вводе: пробелы, отсутствие чисел, деление на ноль.

Словарный калькулятор

Научите бота вычислять математические выражения с целыми числами от одного до десяти, заданные словами. 
Например, “сколько будет три минус два” или “сколько будет четыре умножить на шесть”.
Дополнительно: научите будте обрабатывать вещественные числа (“четыре и пять умножить на шесть и два” – это “4.5 * 6.2”)
'''

import re
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


KEYBOARD = [
    ['7', '8', '9', '*'],
    ['4', '5', '6', '/'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

KEYBOARD_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(b, callback_data=b) for b in row] for row in KEYBOARD])

PATTERN = re.compile(r'\s*(\d*\s*\.{0,1}\s*\d*)\s*([+\-*\/])\s*(\d*\s*\.{0,1}\s*\d*)\s*[=]{0,1}[?]{0,1}\s*')


def do_calculate(user_text):
    match = re.search(PATTERN, user_text)
    
    if match is None:
        raise ValueError('Incorrect input!')
    
    groups = match.groups()
    first_num_str = re.sub('\s*', '', groups[0]) 
    second_num_str = re.sub('\s*', '', groups[2]) 


    if len(first_num_str) == 0 or len(second_num_str) == 0:
        raise ValueError('Incorrect input!')

    first_num = float(first_num_str)
    second_num = float(second_num_str)
    action = groups[1]

    if action == '+':
        return first_num + second_num        
    if action == '-':
        return first_num - second_num
    if action == '*':
        return first_num * second_num
    if action == '/':
        return first_num / second_num

    
def calculate(bot, update, user_data):
    translation = {
        'zero': '0', 
        'one': '1', 
        'two': '2', 
        'three': '3', 
        'four': '4', 
        'five': '5', 
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'plus': '+',
        'minus': '-',
        'multiplied by': '*',
        'divided by': '/',
        'and': '.'
    }

    user_text = update.message.text


    # how much it would be one multiplied by three? ==>  how much it would be 1 * 3
    for k in translation:
        user_text = user_text.replace(k, translation[k])

    try:
        result = do_calculate(user_text)
        update.message.reply_text(str(result))
    except ValueError:
        update.message.reply_text('Incorrect input!')
    except ZeroDivisionError:
        update.message.reply_text('Division by zero!')


def calculate_keyboard(bot, update, user_data):    
    expression = user_data.get('calc_expression', '')
    button = update.callback_query.data
    logging.info("Button pressed: {}".format(button,))

    # если нажали = то вычисляем сохраненное выражение и очищаем сообщение бота Current expression
    if button == '=':
        try:
            result = do_calculate(expression)
            update.callback_query.message.reply_text(str(result))
        except ValueError:
            update.callback_query.message.reply_text('Incorrect input!')
        except ZeroDivisionError:
            update.callback_query.message.reply_text('Division by zero!')

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Current expression:",
            reply_markup=KEYBOARD_MARKUP
        )   
        user_data['calc_expression'] = ''    
        return

    # добавляем к сохраненному выражению нажатую кнопку
    expression += button
    user_data['calc_expression'] = expression

    # редактируем сообщение бота, чтобы вывести текущее выражение
    bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text="Current expression: {}".format(expression,),
         reply_markup=KEYBOARD_MARKUP
    )



