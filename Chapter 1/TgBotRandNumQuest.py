import telebot
import random
from telebot import types

TOKEN = "8703114849:AAE_iLW7x78FNhCieTqoAInnFq-KWhN1Y5s"
bot = telebot.TeleBot(TOKEN)

# Данные игроков: {user_id: {'number': int, 'attempts': int}}
user_data = {}

def get_inline_keyboard():
    markup = types.InlineKeyboardMarkup() #создает кнопку прямо в тектсе
    btn = types.InlineKeyboardButton("Играть", callback_data="start_game") #добавляем кнопку "Играть", единственную
    markup.add(btn)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Угадай число от 1 до 100 за 3 поп итки?", 
        reply_markup=get_inline_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def start_game_callback(call):
    number = random.randint(1, 100)
    user_data[call.message.chat.id] = {'number': number, 'attempts': 3}
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Я загадал число от 1 до 100! Угадай его:"
    )

@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Сначала нажми на кнопку 'Играть!'", reply_markup=get_inline_keyboard())
        return

    if not message.text.isdigit():
        bot.send_message(chat_id, "Введи число цифрами!")
        return

    guess = int(message.text)
    data = user_data[chat_id]
    data['attempts'] -= 1

    if guess == data['number']:
        bot.send_message(chat_id, f"Победа! Это было {guess}. Сыграем еще?", reply_markup=get_inline_keyboard())
        del user_data[chat_id]
    elif data['attempts'] <= 0:
        bot.send_message(chat_id, f"Попытки кончились. Было загадано {data['number']}. Попробуешь снова?", reply_markup=get_inline_keyboard())
        del user_data[chat_id]
    else:
        hint = "Больше ⬆️" if data['number'] > guess else "Меньше ⬇️"
        bot.send_message(chat_id, f"{hint}\nОсталось попыток: {data['attempts']}")

bot.polling(none_stop=True)