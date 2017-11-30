'''
Полнолуние

Научить бота отвечать на вопрос “Когда ближайшее полнолуние после 2016-10-01?”. 
Чтобы узнать, когда ближайшее полнолуние, используй модуль ephem.
'''

import logging
import datetime
import re

import ephem

import common


def constellation(bot, update, user_data):
    planet_name = update.message.text 
    now = datetime.datetime.now()
    try:
        # planet_name = 'Mars' 
        # getattr(ephem, planet_name)(<date>) == ephem.Mars(<date>)
        planet = getattr(ephem, planet_name)(now.strftime('%Y/%m/%d'))
        ephem_answer = ephem.constellation(planet)
        logging.info('Command /planet executed for planet: ' + planet_name)  
        ephem_result = ephem_answer[1]
        update.message.reply_text(planet_name + " in {}".format(ephem_result,) + ' now.' + '\n\n' + common.GREETING)

    except AttributeError:
        update.message.reply_text("I don't know {} planet.".format(planet_name,) + '\n\n' + common.GREETING)


def next_full_moon(bot, update, user_data):
    user_text = update.message.text
    user_date = re.findall(r'\d{4}-\d{2}-\d{2}', user_text) 
        
    if len(user_date) > 0:
        result_date = user_date[0]
    else:
        update.message.reply_text("Date must be in format: YYYY-MM-DD" + '\n\n' + common.GREETING)
        return
        
    result_date = result_date.replace("-", "/")
    ephem_answer = ephem.next_full_moon(result_date)
    update.message.reply_text("The next full moon on {}.".format(ephem_answer,) + '\n\n' + common.GREETING)
