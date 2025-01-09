#импортируем библиотеки
import os
import spacy
import svgwrite
from dotenv import load_dotenv  
import telebot


load_dotenv()

#получаем токен из .env
API_TOKEN = os.getenv("API_TOKEN")

#инициализируем бота
bot = telebot.TeleBot(API_TOKEN)

#загружаем spacy для английского языка
nlp = spacy.load("en_core_web_sm")

#обработчик на получение сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    #получаем текст сообщения
    text = message.text

    #анализируем текст с помощью spacy
    doc = nlp(text)

    #создаем SVG из зависимостей слов
    width = 800
    height = 200
    svg_output = svgwrite.Drawing('dependency.svg', size=(width, height))
    
    x_offset = 50  #начальная координата X
    y = 100       #фиксированная координата Y

    #для каждой зависимости добавляем текст и линию
    for token in doc:
        #добавляем текст токена
        svg_output.add(svgwrite.text.Text(token.text, insert=(x_offset, y), font_size='20px'))

        #если токен имеет родительский токен, добавляем линию
        if token.head != token:  #чтобы не рисовать линию к самому себе
            #определяем координаты для линии от родителя к дочернему
            head_x_offset = 50 + (token.head.i * 100)  #смещение для родительского токена
            svg_output.add(svgwrite.shapes.Line(start=(head_x_offset, y - 10), end=(x_offset, y + 10), stroke=svgwrite.rgb(0, 0, 0, '%')))

        x_offset += 100  #увеличиваем смещение для следующих токенов

    #сохраняем SVG файл
    svg_output.save()

    #отправляем пользователю SVG файл
    with open('dependency.svg', 'rb') as svg_file:
        bot.send_document(message.chat.id, svg_file)

#запускаем бота
bot.polling()