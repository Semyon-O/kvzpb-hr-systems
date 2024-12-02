import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import texts

from logic import komitet_path, apms_path, declaration_path


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Объект бота
bot = Bot(token=os.getenv("TG_TOKEN"))
# Диспетчер
dp = Dispatcher()

dp.include_router(komitet_path.router)
dp.include_router(apms_path.router)
dp.include_router(declaration_path.router)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [types.KeyboardButton(text=texts.vacancies)],
        [types.KeyboardButton(text=texts.faq)],
        [types.KeyboardButton(text=texts.declaration)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "Здравствуйте, это бот по помощи подбору вакансии мировых судей администрации Санкт-Петербург",
        reply_markup=keyboard
    )


@dp.message(lambda c: c.text == texts.vacancies)
async def vacancies(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text=texts.komitet, callback_data=texts.komitet)],
        [types.InlineKeyboardButton(text=texts.administration, callback_data=texts.administration)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)

    await message.answer(
        "Выберите пожалуйста, в какое место вы хотите трудоустроиться",
        reply_markup=keyboard
    )

class FaqState(StatesGroup):
    get_answer = State()

@dp.message(lambda c: c.text == texts.faq)
async def faq(message: types.Message, state: FSMContext):
    await state.clear()

    faq_answer = [
        ("Какие есть вакансии?", "Актуальные вакансии вы можете найти в разделе мировые участки", ),
        ("Как заполнять анкету?", "Актуальная форма заполнения анкеты закреплена в списке документов на прием"),
        ("Какие сроки приема документов на конкурс?", "Сроки приема документов на конкурс до 15 числа каждого месяца."),
        ("Когда конкурс?", "Конкурс проводится ежемесячно в последнюю пятницу месяца."),
        ("Где брать справку по форме 001-гсу?", "Для получения справки по форме 001-гсу необходимо обратиться в районные психоневрологический и наркологический диспансеры по месту регистрации (жительства) или же в частную клинику, у которой есть лицензия на выдачу данных справок. Обращаем ваше внимание, в случае обращения в стороннюю организацию для получения справки 001-гсу, необходимо прикладывать лицензию."),
        ("Где брать заявление на прием и как писать?", "Заявление на прием закреплено в списке документов на прием."),
        ("Куда приезжать на конкурс?", "Конкурс проходит по адресу: г. Санкт-Петербург, ул. Разъезжая, д.26-28, 5 этаж, зал КЧС"),
        ("Нужна ли справка о судимости?", "Не нужна"),
        ("Будет ли учитываться классный чин (выслуга)?", "Да, при приеме на государственную гражданскую службу учитывается выслуга и классный чин Санкт-Петербурга."),
        ("Какие есть ограничения на прием на госслужбу?", "Ограничения, связанные с гражданской службой указаны в статье 16 Федеральный закон от 27.07.2004 № 79-ФЗ «О государственной гражданской службе Российской Федерации»"),
        ("Уведомление кандидата.", "Уведомление о дате, времени и адресе проведения конкурса будет направлено на вашу электронную почту."),
        ("Техническая поддержка", "В случае возникновения сложностей при работе с чат-ботом. "
                                  "Просим вас сообщить об ошибках в данной форме: https://airtable.com/appe3wFxYkIwHibVi/paghg0gv9NwgcR1vW/form")
    ]
    inline_kb_list = []

    for element in range(len(faq_answer)):
        inline_kb_list.append([InlineKeyboardButton(text=faq_answer[element][0], callback_data="get_answer."+str(element))])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_kb_list, resize_keyboard=True)
    await message.answer(
        text="Часто задаваемые вопросы",
        reply_markup=markup
    )


@dp.callback_query(lambda call: call.data.split(".")[0] == "get_answer")
async def answer_on_faq(callback: types.CallbackQuery):
    answer_index = int(callback.data.split(".")[1])

    faq_answer = [
        ("Какие есть вакансии?", "Актуальные вакансии вы можете найти в разделе мировые участки", ),
        ("Как заполнять анкету?", "Актуальная форма заполнения анкеты закреплена в списке документов на прием"),
        ("Какие сроки приема документов на конкурс?", "Сроки приема документов на конкурс до 15 числа каждого месяца."),
        ("Когда конкурс?", "Конкурс проводится ежемесячно в последнюю пятницу месяца."),
        ("Где брать справку по форме 001-гсу?", "Для получения справки по форме 001-гсу необходимо обратиться в районные психоневрологический и наркологический диспансеры по месту регистрации (жительства) или же в частную клинику, у которой есть лицензия на выдачу данных справок. Обращаем ваше внимание, в случае обращения в стороннюю организацию для получения справки 001-гсу, необходимо прикладывать лицензию."),
        ("Где брать заявление на прием и как писать?", "Заявление на прием закреплено в списке документов на прием."),
        ("Куда приезжать на конкурс?", "Конкурс проходит по адресу: г. Санкт-Петербург, ул. Разъезжая, д.26-28, 5 этаж, зал КЧС"),
        ("Нужна ли справка о судимости?", "Не нужна"),
        ("Будет ли учитываться классный чин (выслуга)?", "Да, при приеме на государственную гражданскую службу учитывается выслуга и классный чин Санкт-Петербурга."),
        ("Какие есть ограничения на прием на госслужбу?", "Ограничения, связанные с гражданской службой указаны в статье 16 Федеральный закон от 27.07.2004 № 79-ФЗ «О государственной гражданской службе Российской Федерации»"),
        ("Уведомление кандидата.", "Уведомление о дате, времени и адресе проведения конкурса будет направлено на вашу электронную почту."),
        ("Техническая поддержка", "В случае возникновения сложностей при работе с чат-ботом. "
                                  "Просим вас сообщить об ошибках в данной форме: https://airtable.com/appe3wFxYkIwHibVi/paghg0gv9NwgcR1vW/form")
    ]

    await callback.message.answer(
        text=faq_answer[answer_index][1]
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
