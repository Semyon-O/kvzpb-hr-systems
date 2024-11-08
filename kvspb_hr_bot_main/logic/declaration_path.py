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
        "В рамках поступления на госслужбу вам необходимо составить декларацию о доходах.\n"
        "Для этого вам необходимо воспользоваться программой по составлению декларации о доходах\n\n"
        "Данную программу вы можете получить по это ссылке: http://www.kremlin.ru/structure/additional/12"
    )

    await callback.message.answer(
        "Также для заполнения справки, вам высылается видео инструкция по ее заполнению. Оно доступно по этой ссылке: https://disk.yandex.ru/d/HRKduVqyksUlvg"
    )

    await callback.message.answer(
        "Надеемся, данная инструкция поможет вам быстро заполнить и без проблем предоставить справку БК"
    )
