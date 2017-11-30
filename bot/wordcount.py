'''
Подсчёт количества слов

Добавить команду /wordcount котрая считает сова в присланной фразе. 
Например на запрос /wordcount "Привет как дела" бот должен посчитать количество слов в кавычках и ответить: 3 слова.
Не забудьте: добавить проверки на наличие кавычек, пустую строку. Подумайте, какие еще проверки нужны?
'''

import common

def wordcount(bot, update, user_data):
    intab = '"]}{!@#$%^&*№:,.;\/><+=-_['
    outtab = '                          '

    user_text = update.message.text
    result_user_text = user_text.translate(str.maketrans(intab, outtab))
    user_text_count = len(result_user_text.split())
    update.message.reply_text("There are {} words.".format(user_text_count,) + '\n\n' + common.GREETING)