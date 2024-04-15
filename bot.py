import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

# Нужно вставить токен бота
BOT_TOKEN = '_________'


# URL сайта с вакансиями
VACANCIES_URL = 'https://career.habr.com/vacancies?type=all'

bot = telebot.TeleBot(BOT_TOKEN)

# Функция для парсинга вакансий
def parse_vacancies():
    response = requests.get(VACANCIES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    vacancies = soup.find_all('div', class_='vacancy-card')
    return vacancies

# Обработчик команды /start или нажатия на кнопку "Начать"
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Получить вакансии", callback_data='get_vacancies')
    keyboard.add(button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы получить список вакансий.", reply_markup=keyboard)

# Обработчик нажатия на Inline кнопку "Получить вакансии"
@bot.callback_query_handler(func=lambda call: call.data == 'get_vacancies')
def handle_get_vacancies(call):
    vacancies = parse_vacancies()
    if vacancies:
        for vacancy in vacancies[:5]:  # Limiting to the first 5 vacancies for example
            # Attempt to find the title element using different methods
            title_element = vacancy.find('h3')  # Try finding by 'h3' tag
            if not title_element:
                title_element = vacancy.find(class_='vacancy-card__title')  # Try finding by class
            if not title_element:
                title_element = vacancy.find('a')  # Try finding within anchor tag
            
            if title_element:
                title = title_element.text.strip()
                link = 'https://career.habr.com/vacancies?qid=1&type=all' + str(title_element.get('href'))
                bot.send_message(call.message.chat.id, f'Название: {title}\nСсылка: {link}')
            else:
                bot.send_message(call.message.chat.id, f'Заголовок вакансии не найден.')
    else:
        bot.send_message(call.message.chat.id, "На данный момент вакансий нет.")

# Обработчик команды /vacancies
@bot.message_handler(commands=['vacancies'])
def handle_vacancies(message):
    # Создание Inline кнопки "Получить вакансии"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Получить вакансии", callback_data='get_vacancies')
    keyboard.add(button)
    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы получить список вакансий.", reply_markup=keyboard)

# Запуск бота
bot.polling()
