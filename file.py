from telebot import TeleBot, types
import fitz
from transformers import pipeline

TOKEN = '7402794506:AAGfP5zfrehi1V_uDuHgJkFGcpzzlnaqvI0'
bot = TeleBot(TOKEN)


nlp = pipeline('question-answering', model='deepset/roberta-base-squad2', tokenizer='deepset/roberta-base-squad2', device = 0)

def answer_question_from_pdf(pdf_path, question, window_size=462):
    pdf = fitz.open(pdf_path)
    best_answer = None
    best_confidence = 0

    for page in pdf:
        text = page.get_text()
        for i in range(0, len(text), window_size):
            context = text[i:i+window_size]
            result = nlp(question=question, context=context)
            if result['score'] > best_confidence:
                best_confidence = result['score']
                best_answer = result['answer']

    pdf.close()
    return best_answer


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Дневник')
    itembtn2 = types.KeyboardButton('Экзамены')
    itembtn3 = types.KeyboardButton('Портфолио')
    itembtn4 = types.KeyboardButton('Досуг')
    itembtn5 = types.KeyboardButton("ЧаВо")
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, "Привет! Как я могу тебе помочь?", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def on_message(message):
    if message.text == 'Дневник':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Добавить оценки вручную')
        itembtn2 = types.KeyboardButton('Привязать дневник')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, 'Добро пожаловать в раздел "Дневник"!', reply_markup=markup)
    elif message.text == 'Экзамены':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Спросить у ИИ')
        itembtn2 = types.KeyboardButton('Прорешать задачи')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, 'Добро пожаловать в раздел "Экзамены"!', reply_markup=markup)
    elif message.text == 'Спросить у ИИ':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Спросить у ИИ')
        itembtn2 = types.KeyboardButton('Прорешать задачи')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, "Введите ваш вопрос:\n\nP.S. Модель, используемая для демонстрации понимает только английский язык и отвечает на вопросы по статье о новой архитектуре нейросетей - KAN. Вы можете ознакомиться с ней ниже.")
        with open('lp.pdf', 'rb') as pdf_file:
          bot.send_document(message.chat.id, pdf_file)
        bot.register_next_step_handler(message, ask_roberta)
    elif message.text == 'Прорешать задачи':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Спросить у ИИ')
        itembtn2 = types.KeyboardButton('Прорешать задачи')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, "Вот несколько ресурсов:\n*Для сдачи ОГЭ*\n1. https://oge.sdamgia.ru/?redir\n2. https://fipi.ru/oge/\n3. https://synergy.ru/edu/oge\n\n*Для сдачи ЕГЭ*\n1. https://ege.sdamgia.ru/\n2. https://fipi.ru/ege\n3. https://neznaika.info/ege/", reply_markup=markup)
    elif message.text == 'Портфолио':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Добавить достижения вручную')
        itembtn2 = types.KeyboardButton('Привязать аккаунты')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, 'Добро пожаловать в раздел "Портфолио"!', reply_markup=markup)
    elif message.text == 'Досуг':
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Найти спортивные мероприятия')
        itembtn2 = types.KeyboardButton('Получить советы о досуге')
        itembtn3 = types.KeyboardButton('Назад')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, 'Добро пожаловать в раздел "Досуг"!', reply_markup=markup)
    elif message.text == "ЧаВо":
        bot.send_message(message.chat.id, "Это цифровой помощник школьника, который поможет в повседневной жизни! Давай пройдемся по его разделам:\n*Дневник*\nВ этом разделе ты сможешь получить доступ к своим оценкам и домашнему заданию. Заполняй дневник вручную или связывай профили!\n*Экзамены*\nТут ты можешь прорешать задания интересующего тебя предмета или задать по нему вопрос\n*Портфолио*\nЗайдя в этот раздел ты увидишь свои академические и личностные достижения а также персональные рекомендации по дополнительному образованию\n*Досуг*\nЗдесь находятся спортивные мероприятия, советы по досугу а также твой виртуальный друг, с которым можно просто поболтать", parse_mode = "Markdown")
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Дневник')
        itembtn2 = types.KeyboardButton('Экзамены')
        itembtn3 = types.KeyboardButton('Портфолио')
        itembtn4 = types.KeyboardButton('Досуг')
        itembtn5 = types.KeyboardButton("ЧаВо")
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        bot.send_message(message.chat.id, "Привет! Как я могу тебе помочь?", reply_markup=markup)

def ask_roberta(message):
    question = message.text
    pdf_path = 'lp.pdf'
    answer = answer_question_from_pdf(pdf_path, question)
    bot.send_message(message.chat.id, answer)
    print(answer)

bot.polling()
