from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext


import texts

router = Router()


@router.message(lambda c: c.text == texts.declaration)
async def on_declaration_button(message: types.Message, state: FSMContext):
    await state.clear()
    kb = [
        [types.InlineKeyboardButton(text="В рамках декларации компании", callback_data="company")],
        [types.InlineKeyboardButton(text="В рамках поступлении на госслужбу", callback_data="gos_work")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)

    await message.answer(
        "Выберите пожалуйста, в рамках чего вы хотите отправить декларацию",
        reply_markup=keyboard
    )


@router.callback_query(lambda msg: msg.data == 'gos_work')
async def on_gos_work_button(callback: types.CallbackQuery, bot: Bot):
    await callback.message.answer(
        "В рамках поступления на госслужбу вам необходимо составить декларацию о доходах.\n\n"
        "Для этого вам необходимо воспользоваться программой по составлению декларации о доходах.\n\n"
        "Данную программу вы можете получить по это ссылке: http://www.kremlin.ru/structure/additional/12"
    )

    url_list = {
        "1. Титульный лист справки": "https://disk.yandex.ru/i/v8KqEgp0Jt00Lw",
        "2. Раздел 1. Сведения о доходах": "https://disk.yandex.ru/i/DWn4bdj5KrE3CQ",
        "3. Раздел 2. Сведения о расходах": "https://disk.yandex.ru/i/34ZQ2Ee-rcZWYQ",
        "4. Раздел 3.2. Сведения о транспортных средствах": "https://disk.yandex.ru/i/LfqPcHrANHX1pA",
        "5. Раздел 3.3. Сведения о финансовых активах": "https://disk.yandex.ru/i/-K9aXep96o1aQg",
        "6. Раздел 5. Сведения о ценных бумагах": "https://disk.yandex.ru/i/IN91Xl7BxHzJrg",
        "7. Раздел 6. Сведения об обязательствах имущественного характера": "https://disk.yandex.ru/i/jLXlGq9sliryBw",
        "8. Раздел 6.1. Сведения об объектах недвижимости": "https://disk.yandex.ru/i/k45PPssnNVu8Rw",
        "9. Раздел 6.2. Сведения о финансах": "https://disk.yandex.ru/i/hTcco8IZ4fczYQ",
        "9.1. Раздел 7. Безвозмездные сделки": "https://disk.yandex.ru/i/Bgz3SC4Detbw-Q",
        "10. Заключение": "https://disk.yandex.ru/i/AQf-wqf9nWx4Ew",
    }

    urls_buttons = [[types.InlineKeyboardButton(text=str(text), url=url)] for text, url in url_list.items()]
    markup = types.InlineKeyboardMarkup(inline_keyboard=urls_buttons, resize_keyboard=True)

    await callback.message.answer(
        "Также для заполнения справки, вам высылается видео инструкция по ее заполнению.",
        reply_markup=markup,

    )

    await callback.message.answer(
        "Надеемся, данная инструкция поможет вам быстро заполнить и без проблем заполнить справку БК"
    )
