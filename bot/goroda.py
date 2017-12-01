'''
Научите бота играть в города. Правила такие - внутри бота есть список городов, 
пользователь пишет /goroda Москва и если в списке такой город есть, бот отвечает городом на букву "а" - "Альметьевск, ваш ход". 
Оба города должны удаляться из списка.
'''
import random

def find_city(last_letter, current_available_cities):
    for bot_city in current_available_cities:
        if bot_city.startswith(last_letter):
            return bot_city
    return None


def get_last_letter(word):
    if word[-1] in ['ь', 'ъ', 'ы']:
        return word[-2]
    return word[-1]
        

def goroda(bot, update, user_data):
    user_city = update.message.text.lower()

    if len(user_city.split()) != 1:
        update.message.reply_text('Incorrect input!')
        return

    # если ключ 'cities'не в user_data
    if 'cities' not in user_data:
        with open('city.csv', 'rt') as f:
            cities = []
            for line in f:
                line = line.replace('\n', '').lower()
                cities.append(line)
            # в user_data появляется ключ 'cities', значение - массив всех городов (cities[])
            random.shuffle(cities)
            user_data['cities'] = cities

    # записываем в переменную current_available_cities (это массив) не вычеркнутые города из user_data 
    current_available_cities = user_data['cities']

    last_bot_city = user_data.get('last_bot_city', None)

    if last_bot_city is not None:
        last_letter = get_last_letter(last_bot_city)
        if user_city[0] != last_letter:
            update.message.reply_text("Твой город должен начинаться с буквы {}!".format(last_letter.upper(),))
            return

    if user_city not in current_available_cities:
        update.message.reply_text('Такого города нет или уже назывался!')
        return

    # если город в списке, вычеркиеваем его из current_available_cities
    current_available_cities.remove(user_city) 

    last_letter = get_last_letter(user_city)

    bot_city = find_city(last_letter, current_available_cities)
    if bot_city is not None:
        user_data['last_bot_city'] = bot_city
        current_available_cities.remove(bot_city) 
        update.message.reply_text(bot_city.capitalize() + '\n\n' + 'Твой ход!')
        random.shuffle(current_available_cities)
        return

    update.message.reply_text('Поздравляю, ты выиграл!')
    user_data.clear()














            



