import common

def wordcount(bot, update, user_data):
    intab = '"]}{!@#$%^&*№:,.;\/><+=-_['
    outtab = '                          '

    user_text = update.message.text
    result_user_text = user_text.translate(str.maketrans(intab, outtab))
    user_text_count = len(result_user_text.split())
    update.message.reply_text("There are {} words.".format(user_text_count,) + '\n\n' + common.GREETING)