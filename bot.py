# telegram bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import common
import astronomy
import wordcount
import calculator

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log')


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
        'greeting': 'Send me an arithmetic expression in the format: a+b=', 
        'action': calculator.calculate
    },
}


def command_factory(name):        
    '''
    Функция "фабрика", создающая функции обработчики для каждой команды с именем "name"
    '''
    def command(bot, update, user_data):
        # Обработка всех входящих команд
        update.message.reply_text(COMMAND_REGISTRY[name]['greeting'])
        user_data['mode'] = name
    return command

def text(bot, update, user_data):
    # Обработка входящего текста (роутер)
    mode = user_data.get('mode', None) 
    
    if mode is None:
        update.message.reply_text(common.GREETING)
        return

    action = COMMAND_REGISTRY[mode]['action']
    if action is None:
        update.message.reply_text(common.GREETING)
        return

    action(bot, update, user_data)

def exit(bot, update, user_data):
    user_data['mode'] = None
    update.message.reply_text(common.GREETING)

def main():
    updater = Updater('467895224:AAF110ARNylzxt_CVZkcp3rAbdtSktjBquM')

    dp = updater.dispatcher
    for command_name in COMMAND_REGISTRY:
        '''
        command_factory(command_name) - реагировать результатом вызова функции command_factory 
        (а результат вызова - это функция command, вложенная в command_factory)
        '''
        action = command_factory(command_name) 
        dp.add_handler(CommandHandler(command_name, action, pass_user_data=True))
    dp.add_handler(CommandHandler('exit', exit, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, text, pass_user_data=True))

    updater.start_polling()
    updater.idle()


main()
