'''
Возьмите словарь с ответами из функции get_answer
Запишите его содержимое в формате csv в формате: "ключ"; "значение". 
Каждая пара ключ-значение должна располагаться на отдельной строке.
'''
import csv

answers = {
    "Привет": "Здравствуй!", 
    "Как дела?": "Хорошо!",
    "Что делаешь?": "Работаю", 
    "Пойдем гулять?": "С удовольствием!",
    "Пока": "Увидимся!"
}


with open('export.csv', 'w', encoding='utf-8-sig') as f:
    writer = csv.writer(f, dialect='excel', delimiter=';')
    for answer in answers:
        writer.writerow([answer, answers[answer]])
