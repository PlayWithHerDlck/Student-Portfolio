import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "TG_Bot_Token"
bot = Bot(token=TOKEN)
dp = Dispatcher()

QUIZ_DATA = [
    {"question": "Какой ресурс нужен для приручения Аргентависа?", "options": {"Жареное мясо": 0, "Superior Kibble": 1, "Ягоды": 0}},
    {"question": "Как называется первый босс на The Island?", "options": {"Роквелл": 0, "Дракон": 0, "Брутматер": 1}},
    {"question": "Кто лучше всех собирает металл?", "options": {"Анкилозавр": 1, "Додикурус": 0, "Трайк": 0}},
    {"question": "Что нужно для дыхания под водой?", "options": {"Ласты": 0, "Баллон": 1, "Маска": 0}},
    {"question": "Кто ворует вещи из инвентаря?", "options": {"Пегомастакс": 1, "Дилофозавр": 0, "Раптор": 0}},
    {"question": "Самый прочный материал для базы?", "options": {"Камень": 0, "Железо": 0, "Тек": 1}},
    {"question": "Кто лучше всех собирает солому?", "options": {"Олень": 1, "Стегозавр": 0, "Мамонт": 0}},
    {"question": "Светящиеся существа из Aberration — это...", "options": {"Жнецы": 0, "Светопитомцы": 1, "Безымянные": 0}},
    {"question": "Что восстанавливает выносливость?", "options": {"Стимулятор": 1, "Наркоберри": 0, "Мясо": 0}},
    {"question": "Зачем нужен Овираптор?", "options": {"Сбор дерева": 0, "Яйценоскость": 1, "Охрана": 0}},
]

user_scores = {}

def get_quiz_keyboard(question_index):
    builder = InlineKeyboardBuilder()
    for text, points in QUIZ_DATA[question_index]["options"].items():
        # Передаем текст ответа и баллы
        builder.button(text=text, callback_data=f"ans_{question_index}_{points}_{text}")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def start_quiz(message: types.Message):
    user_scores[message.from_user.id] = 0
    await message.answer("👋 Привет! Я — ARK Quiz Bot Я помогу проверить, насколько хорошо ты знаешь мир выживания.")
    await send_question(message.from_user.id, 0)

async def send_question(user_id, question_index):
    question = QUIZ_DATA[question_index]["question"]
    await bot.send_message(user_id, f"<b>Вопрос №{question_index + 1}:</b>\n{question}", 
                           reply_markup=get_quiz_keyboard(question_index), parse_mode="HTML")

@dp.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: types.CallbackQuery):
    # Разбираем данные: индекс, баллы, текст ответа
    _, q_index, points, answer_text = callback.data.split("_")
    q_index, points = int(q_index), int(points)
    user_id = callback.from_user.id

    # 1. Выводим выбор пользователя
    await callback.message.answer(f"🗨 Мой ответ: {answer_text}")

    # 2. Проверяем правильность
    if points > 0:
        user_scores[user_id] = user_scores.get(user_id, 0) + 1
        await callback.message.answer("✅ Правильно!")
    else:
        # Ищем правильный вариант в QUIZ_DATA для этого вопроса
        correct_answer = ""
        for text, p in QUIZ_DATA[q_index]["options"].items():
            if p == 1:
                correct_answer = text
                break
        await callback.message.answer(f"❌ Неправильно. Правильный ответ: <b>{correct_answer}</b>", parse_mode="HTML")

    # Убираем кнопки у текущего вопроса
    await callback.message.edit_reply_markup(reply_markup=None)

    # 3. Переход к следующему вопросу
    next_index = q_index + 1
    if next_index < len(QUIZ_DATA):
        await send_question(user_id, next_index)
    else:
        total = user_scores.get(user_id, 0)
        await bot.send_message(user_id, f"🏆 Тест завершен! Твой результат: {total} из {len(QUIZ_DATA)}.")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())