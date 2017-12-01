# telegram bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging

import common
import astronomy
import wordcount
import calculator
import goroda

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
                    # filename='bot.log')


COMMAND_REGISTRY = {
    'start': {
        'greeting': common.GREETING, 
        'action': None
    },
    'planet': {
        'greeting': 'What planet are you interested in?', 
        'action': astronomy.constellation
    },
    'wordcount': {
        'greeting': 'Say me anything!', 
        'action': wordcount.wordcount
    },
    'next_full_moon': {
        'greeting': 'Send me date in format: YYYY-MM-DD', 
        'action': astronomy.next_full_moon
    },
    'calculator': {
        'greeting': "You can use '+', '-', '*', '/'. \nSend me an arithmetic expression or ask me: What is the value of two plus/minus/multiplied by/divided by three?", 
        'action': calculator.calculate,
        'keyboard': calculator.KEYBOARD_MARKUP,
    },
    'goroda': {
        'greeting': 'Поиграем в города. Ты начинаешь!',
        'action': goroda.goroda
    }
}


class ModeChooser(object):
    def __init__(self, command_name):
        self.command_name = command_name

    def do(self, bot, update, user_data):
        logging.info('Command {} entered'.format(self.command_name,))
        # обработчик
        keyboard = COMMAND_REGISTRY[self.command_name].get('keyboard', None)
        update.message.reply_text(COMMAND_REGISTRY[self.command_name]['greeting'], reply_markup=keyboard)        
        user_data['mode'] = self.command_name


def text(bot, update, user_data):
    # Обработка входящего текста (маршрутизатор)
    mode = user_data.get('mode', None) 
    
    if mode is None:
        update.message.reply_text(common.GREETING)
        return

    action = COMMAND_REGISTRY[mode]['action']
    if action is None:
        update.message.reply_text(common.GREETING)
        return

    action(bot, update, user_data)


def keyboard_action(bot, update, user_data):
    logging.info('Keyboard action')
    mode = user_data.get('mode', None)    
    if mode == 'calculator':
        calculator.calculate_keyboard(bot, update, user_data)


def exit(bot, update, user_data):    
    # user_data['mode'] = None, но очищаем вообще весь словарь
    user_data.clear()
    update.message.reply_text(common.GREETING)

def main():
    updater = Updater('467895224:AAF110ARNylzxt_CVZkcp3rAbdtSktjBquM')
    dp = updater.dispatcher

    for command_name in COMMAND_REGISTRY:
        # создаем объект класса Action для command_name, чтобы сохранить command_name для вызова обработчика action.do,
        # потому что handler общий для всех команд
        chooser = ModeChooser(command_name)
        dp.add_handler(CommandHandler(command_name, chooser.do, pass_user_data=True))

    dp.add_handler(CommandHandler('exit', exit, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, text, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(keyboard_action, pass_user_data=True))

    updater.start_polling()
    updater.idle()


main()
