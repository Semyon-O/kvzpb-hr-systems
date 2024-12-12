import logging
import os

from aiogram import Router, types, Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender, logger

import texts
import services
from services import get_unique_data_by_field
import requests

router = Router()

current_file_path = __file__
directory_path = os.path.dirname(current_file_path)

class PostAnketaStates(StatesGroup):
    choose_district = State()
    choose_judgment_area = State()
    get_info_about_place = State()
    register_hr_site = State()
    start_filling_anket = State()
    user_send_docs = State()
    user_collected_all_docs = State()
    enter_fio = State()


class BookingVisitor(StatesGroup):
    start_booking = State()
    enter_fio = State()
    choose_time_visit_bk = State()
    confirm_windows_bk = State()
    time_visit_hr = State()


@router.callback_query(lambda msg: msg.data == texts.administration)
async def choose_post_handler(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f"choose_post_handler. user {callback.from_user.id}. data: {callback.data}")

    posts = get_unique_data_by_field("Должность", services.fetch_available_posts)

    kb = [[types.InlineKeyboardButton(text=post.capitalize(), callback_data=post)] for post in posts]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)


    await callback.message.answer(
        text="Выберите пожалуйста интересущую вас должность из списка ниже",
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.choose_district)


@router.callback_query(PostAnketaStates.choose_district)
async def choose_district_handler(callback: types.CallbackQuery, state: FSMContext):

    await state.update_data(post=callback.data)

    districts = get_unique_data_by_field("Район", services.fetch_persons_info)

    kb = [[types.InlineKeyboardButton(text=district, callback_data=district)] for district in districts]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="Выберите пожалуйста в каком районе вы хотели-бы рассмотреть работу?",
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.choose_judgment_area)


@router.callback_query(PostAnketaStates.choose_judgment_area)
async def choose_district_judgment_area_handler(callback: types.CallbackQuery, state: FSMContext):

    # search['district'] = callback.data
    await state.update_data(district=callback.data)
    search = await state.get_data()
    districts = services.fetch_judgment_places(search["post"], search["district"])

    if not districts:
        await callback.message.answer(
                text="Извините, в выбранной области нет доступных участков.")
        return


    kb = [[types.InlineKeyboardButton(text=f"Участок №{district}", callback_data=str(district))] for district in districts]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="Выберите пожалуйста в какой участок вы хотите отправить данные?",
        reply_markup=markup
    )
    await state.set_state(PostAnketaStates.get_info_about_place)


@router.callback_query(PostAnketaStates.get_info_about_place)
async def choose_area_handler(callback: types.CallbackQuery, state: FSMContext):
    id_district = callback.data

    judgment_place = services.fetch_persons_info(filters="filterByFormula={Участок}=" + id_district)


    kb = [
        [types.InlineKeyboardButton(text="Подать документы на этот участок", callback_data=str(id_district))]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    data = judgment_place[0]['fields']
    await callback.message.answer(
        text=f"""<b>Информация по участку</b>\n
        <b>ФИО мирового судьи:</b> \n{data["ФИО судьи"]}
        <b>Телефон:</b> {data["Телефон"]}
        <b>Адрес участка:</b> {data["Адрес"]}
        <b>Район:</b><i>{data["Район"].title()}</i>\n
        """,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )
    await state.set_state(PostAnketaStates.register_hr_site)

@router.callback_query(PostAnketaStates.register_hr_site)
async def start_instruction(callback: types.CallbackQuery, state: FSMContext):
    id_judgement_place = callback.data
    kb = [
        [types.InlineKeyboardButton(text="Авторизоваться", url="https://hr.gov.spb.ru/vakansii/?")],
        [types.InlineKeyboardButton(text="Я заполнил анкету на сайте", callback_data=id_judgement_place)],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)

    await callback.message.answer(
        "Для создания анкеты в комитет. Нужно зарегистрироваться или авторизоваться на сайте комитета."
        "\nПройдите пожалуйста, регистрацию или авторизацию. И затем заполните анкету для конкурса.\n"
        "\nЕсли вы прошли авторизацию и заполнили анкету, нажмите на кнопку '<b>Я заполнил анкету на сайте</b>'",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(PostAnketaStates.start_filling_anket)

@router.callback_query(PostAnketaStates.start_filling_anket)
async def filling_anket(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    id_judgement_place = callback.data

    await state.update_data(id_judgement_place=id_judgement_place)

    judgment_place = services.fetch_persons_info(filters="filterByFormula={Участок}=" + id_judgement_place)

    data = judgment_place[0]['fields']

    await callback.message.answer(
        text="После заполнения анкеты. Вам необходимо заполнить следующие документы:"
    )

    documents = [
        FSInputFile(directory_path+"/pattern_documents/Анкета.docx"),
        FSInputFile(directory_path+"/pattern_documents/Заявка на секретаря суда.doc"),
        FSInputFile(directory_path+"/pattern_documents/Заявка на секретаря суд. заседания.doc"),
        FSInputFile(directory_path+"/pattern_documents/Список документов на конкурс.doc"),
    ]
    media_docs = []
    for document_to_send in documents:
        media_docs.append(
            types.InputMediaDocument(media=document_to_send)
        )

    chatActionSender = ChatActionSender(
        bot=bot,
        chat_id=callback.message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )

    async with chatActionSender as action:
        await bot.send_media_group(callback.message.chat.id, media=media_docs)

    kb = [
        [types.InlineKeyboardButton(text="Я отправил документы ответственному", callback_data=str(id_judgement_place))]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="После заполнение документов, вам необходимо отправить их на почту ответственного по участку:"
             # f"\n<b>ФИО ответственного:</b> {data['Сотрудник, ответственный за участок']}"
             # f"\n<b>Почта ответственного:</b> {data['Почта']}",
             f"\n<b>ФИО ответственного:</b> Дупленский Роман Сергеевич"
             f"\n<b>Почта ответственного:</b> duplenskiy@zakon.gov.spb.ru",
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

    await state.update_data(email=data["Почта"])
    await state.set_state(PostAnketaStates.user_send_docs)


@router.callback_query(PostAnketaStates.user_send_docs)
async def info_about_tender(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

    kb = [
        [types.InlineKeyboardButton(text="Я прошел конкурс", callback_data="data")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="""Отлично!\n 
        Информируем Вас, что конкурс состоится в последнюю пятницу месяца.\n
        В случае изменения даты и времени будет сообщено дополнительно \n
        Начало 9:20 по адресу: г. Санкт-Петербург, ул. Разъезжая, д. 26-28, 5 этаж, зал КЧС.\n 
        О дате и проведении конкурса вы будете уведомлены дополнительно по адресу вашей электронной почты \n
        С собой: паспорт и ручка\n
        """,
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.user_collected_all_docs)


@router.callback_query(PostAnketaStates.user_collected_all_docs)
async def filling_work_docs(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

    await callback.message.answer(
        text="""
        Наши поздравления!\n\nДля поступления на государственную гражданскую службу необходимо предоставить следующие документы.
        """
    )

    kb = [
        [types.InlineKeyboardButton(text="Я собрал все документы", callback_data="data")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    documents = [
        FSInputFile(directory_path+"/hiring_docs/Заявление на прием.doc"),
        FSInputFile(directory_path+"/hiring_docs/Список док-ов на прием.doc")
    ]
    media_docs = []
    for document_to_send in documents:
        media_docs.append(
            types.InputMediaDocument(media=document_to_send)
        )
    await callback.message.answer(
        text="Документы, которые нужно заполнить для трудоустройства",
    )
    await bot.send_media_group(callback.message.chat.id, media=media_docs)

    await callback.message.answer(
        "Также обращаем ваше внимание на заполнение справки о доходах и расходах. Перед заполнением ознакомьтесь с инструкцией,"
        "которая доступна по ссылке: https://disk.yandex.ru/d/HRKduVqyksUlvg",
        reply_markup=markup,

    )

    await state.set_state(BookingVisitor.start_booking)


@router.callback_query(BookingVisitor.start_booking)
async def start_booking(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(
        "Отлично. Теперь вам нужно выбрать удобные окна времени посещения:\n"
        "- К специалисту по заполнению справки о доходах и расходах\n"
        "- К кадровому специалисту для трудоустройства \n"
    )
    await callback.message.answer(
        "Для начала выбора окон времени напишите полностью Вашу Фамилию, Имя, Отчество"
    )
    await state.set_state(BookingVisitor.enter_fio)


@router.message(BookingVisitor.enter_fio)
async def enter_fio_and_getting_windows_bk(message: types.Message, state: FSMContext, *args, **kwargs):

    fio_person = message.text

    await state.update_data(fio_person=fio_person)

    kb =types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Выбрать окно времени', callback_data="choose_time"),],
        ]
    )
    await message.answer("Теперь вам нужно выбрать время записи к специалисту по справке БК", reply_markup=kb)
    await state.set_state(BookingVisitor.choose_time_visit_bk)



@router.callback_query(BookingVisitor.choose_time_visit_bk)
async def getting_windows_bk(callback: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    state_data = await state.get_data()

    data = callback.data
    bk_person = "a.starinskaya@zakon.gov.spb.ru"

    try:
        if data.startswith("choose_time"):
            response = requests.get(
                f"http://localhost:8000/api/free-time-windows?email={bk_person}"
            )

            if response.json() == []:
                raise ValueError

            kb = [[types.InlineKeyboardButton(text=f"{date['date']} (с {date['time_start']} до {date['time_end']})", callback_data=f"taken:{date['id']}")] for date in response.json()]
            markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await callback.message.answer(
                text="Выберите пожалуйста удобные вам окна",
                reply_markup=markup,
            )
        if data.startswith("taken"):
            print(data)
            await callback.message.answer(
                f"Подтверждаете ли выбранное время?",
                reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text='Да, подтверждаю', callback_data=f"accept:{data.split(":")[1]}"),],
                    [types.InlineKeyboardButton(text='Нет, выберу другое', callback_data="choose_time"),],
                ]
            )
        )
        if data.startswith("accept"):
            state_data = await state.get_data()
            taken_time = data.split(":")[1] # accept:N
            print("State",state_data)

            response = requests.post(
                f"http://localhost:8000/api/take-time-windows",
                data={
                    "person_data": state_data["fio_person"],
                    "telegram_nickname": callback.message.from_user.username,
                    "id_judgement_place": int(state_data["id_judgement_place"]),
                    "taken_time": taken_time,
                }
            )

            if response.status_code in (404, 400, ):
                raise Exception

            await callback.message.answer("Очередь на запись к специалисту  по справкам о доходах и расходах оформлена.")
            await callback.message.answer(
                "Теперь вам нужно выбрать окно времени для посещения к кадровому специалисту",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text='Выбрать окно времени', callback_data="choose_time_hr"),],
                    ]
                )
            )
            await state.set_state(BookingVisitor.time_visit_hr)
    except ValueError as e:
        await callback.message.answer(
            text="Извините пожалуйста, но на данный момент пока нету свободных окон. \n"
                 "В случае отсутствия окон, позвоните пожалуйста в сектор кадрового обеспечения по телефону: +7 (812) 576-6098."
        )
        await callback.message.answer(
            "Выберите удобное окно времени для посещения к кадровому специалисту",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text='Выбрать окно времени', callback_data="choose_time_hr"), ],
                ]
            )
        )
        await state.set_state(BookingVisitor.time_visit_hr)
    except Exception as e:
        logging.critical("CRITICAL error", exc_info=e)
        await callback.message.answer(
            "Извините пожалуйста, но входе отправки данных произошла ошибка. Мы занимаемся ее устранением."
        )


@router.callback_query(BookingVisitor.time_visit_hr)
async def getting_windows_hr(callback: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    state_data = await state.get_data()
    data = callback.data

    try:
        if data.startswith("choose_time"):
            response = requests.get(
                f"http://localhost:8000/api/free-time-windows?email={state_data['email']}"
            )

            if response.json() == []:
                raise ValueError

            kb = [[types.InlineKeyboardButton(text=f"{date['date']} (с {date['time_start']} до {date['time_end']})",
                                              callback_data=f"taken:{date['id']}")] for date in response.json()]
            markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await callback.message.answer(
                text="Выберите пожалуйста удобные вам окна",
                reply_markup=markup,
            )
        if data.startswith("taken"):
            await callback.message.answer(
                f"Подтверждаете ли выбранное время?",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text='Да, подтверждаю',
                                                    callback_data=f"accept:{data.split(":")[1]}"), ],
                        [types.InlineKeyboardButton(text='Нет, выберу другое', callback_data="choose_time"), ],
                    ]
                )
            )
        if data.startswith("accept"):
            state_data = await state.get_data()
            taken_time = data.split(":")[1]  # accept:N
            print("State", state_data)

            response = requests.post(
                f"http://localhost:8000/api/take-time-windows",
                data={
                    "person_data": state_data["fio_person"],
                    "telegram_nickname": callback.message.from_user.username,
                    "id_judgement_place": int(state_data["id_judgement_place"]),
                    "taken_time": taken_time,
                }
            )

            if response.status_code in (404, 400,):
                raise Exception

            await callback.message.answer(
                "Очередь на запись к кадровому специалисту оформлена")
            await callback.message.answer(
                "Спасибо, что записались на прием.\n"
                "Ждем вас по адресу: \n"
                "191060, г. Санкт-Петербург, проезд. Смольный, д. 1, лит. Б, 6 подъезд.",
            )
            await state.clear()

    except ValueError as e:
        await callback.message.answer(
            text="Извините пожалуйста, но на данный момент пока нету свободных окон. \n"
                 "Попробуйте запросить информацию позднее повторно нажав на кнопку 'Выбрать окно времени'"
        )

        await callback.message.answer(
            "Выберите удобное окно времени для посещения к кадровому специалисту",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text='Выбрать окно времени', callback_data="choose_time_hr"), ],
                ]
            )
        )
    except Exception as e:
        logging.critical("CRITICAL error", exc_info=e)
        await callback.message.answer(
            "Извините пожалуйста, но входе отправки данных произошла ошибка. Мы занимаемся ее устранением."
        )
# @router.callback_query(FilterByStateAndData(BookingVisitor.choose_time_visit, ""))
# async def get_free_time_visit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
#
#     state_data = await state.get_data()
#
#     try:
#         response = requests.get(
#             f"http://backend:8000/api/free-time-windows?email={state_data['email']}"
#         )
#
#         if response.json() == []:
#             raise ValueError
#
#         kb = [[types.InlineKeyboardButton(text=f"{date['date']} (с {date['time_start']} до {date['time_end']})", callback_data=f"{date['id']}")] for date in response.json()]
#         markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
#
#         await callback.message.answer(
#             "Выберите доступные даты и время для посещения",
#             reply_markup=markup
#         )
#         await state.set_state(BookingVisitor.accept_time_visit)
#
#     except ValueError:
#         logging.info(f"No time windows. Data: {state_data}", exc_info=True)
#         await callback.message.answer("Приносим свои извинения, но на данный момент, выбрать время окон нельзя."
#                                       "Попробуйте отправить запрос позднее")
#         await state.set_state(BookingVisitor.choose_time_visit)
#     except Exception as e:
#         logging.error(f"Exception occurred from get_free_time_visit. Data {state_data}", exc_info=e)
#         await callback.message.answer("Приносим свои извинения, но входе обработки данных, возникла ошибка")
#         await state.set_state(BookingVisitor.choose_time_visit)
#
#
# @router.callback_query(BookingVisitor.accept_time_visit)
# async def choose_time_visit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
#     time_ticket = callback.data
#     await state.update_data(time_ticket=time_ticket)
#     await callback.message.answer("Отлично. Теперь введите ваше ФИО")
#     await state.set_state(BookingVisitor.enter_fio)
#
#
# @router.message(F.text,BookingVisitor.enter_fio)
# async def enter_fio(message: types.Message, state: FSMContext, bot: Bot):
#     fio = message.text
#
#     collected_data = await state.get_data()
#
#     try:
#         response = requests.post(
#             f"http://backend:8000/api/take-time-windows",
#             data={
#                 "person_data": fio,
#                 "telegram_nickname": message.from_user.username,
#                 "id_judgement_place": int(collected_data["id_judgement_place"]),
#                 "taken_time": collected_data["time_ticket"],
#             }
#         )
#
#         if response.status_code in (404, 400, ):
#             raise Exception
#
#         await message.answer("Ваша очередь оформлена на выбранное вами время.\n\n"
#                              "Ждем вас по адресу:\n"
#                              "191060, г Санкт-Петербург,проезд Смольный, д.1, лит.Б, 6 подъезд")
#     except Exception as e:#
#        logging.critical("Lost connection with server", exc_info=e)
#        await message.answer("Приносим свои извинения, но входе обработки данных, возникла ошибка")