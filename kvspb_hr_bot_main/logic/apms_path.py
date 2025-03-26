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


router = Router()

current_file_path = __file__
directory_path = os.path.dirname(current_file_path)


class PostAnketaStates(StatesGroup):
    choose_district = State()
    choose_judgment_area = State()
    get_info_about_place = State()
    register_hr_site = State()
    fio_ask = State()
    email_ask = State()
    # email_confirm = State()
    start_filling_anket = State()
    user_send_docs = State()
    user_waiting_anket = State()
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
    posts = services.fetch_available_posts()
    logging.info(f"ПОСТс {posts}")

    kb = [[types.InlineKeyboardButton(text=post['name'], callback_data=str(post['id']))] for post in posts]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="Выберите пожалуйста интересующую вас должность из списка ниже",
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.choose_district)


@router.callback_query(PostAnketaStates.choose_district)
async def choose_district_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(post=callback.data)

    districts = services.fetch_persons_info(callback.data)

    kb = [[types.InlineKeyboardButton(text=district["name"], callback_data=district["name"])] for district in districts]
    kb.append(
        [types.InlineKeyboardButton(text='Выбрать другую должность', callback_data='another_post')]
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="Выберите пожалуйста в каком районе вы хотели-бы рассмотреть работу?",
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.choose_judgment_area)


@router.callback_query(PostAnketaStates.choose_judgment_area)
async def choose_district_judgment_area_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'another_post':
        posts = services.fetch_available_posts()
        kb = [[types.InlineKeyboardButton(text=post['name'], callback_data=str(post['id']))] for post in posts]
        markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

        await callback.message.answer(
            text="Выберите пожалуйста интересующую вас должность из списка ниже",
            reply_markup=markup
        )

        await state.set_state(PostAnketaStates.choose_district)

        return

    # search['district'] = callback.data
    await state.update_data(district=callback.data)
    search = await state.get_data()
    post = search["post"]
    district = search["district"]

    districts = services.fetch_judgment_places(district, int(post))
    logging.info(f"ПОСТс {districts}")

    if not districts:
        await callback.message.answer(
            text="Извините, в выбранной области нет доступных участков.")
        return

    kb = [
        [types.InlineKeyboardButton(text="Участок №" + str(district["id_judgment"]),
                                    callback_data=str(district["id_judgment"]))] for district in districts
    ]
    kb.append(
        [types.InlineKeyboardButton(text=f"Выбрать другой район поиска", callback_data="another_area_district")]
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="Выберите пожалуйста в какой участок вы хотите отправить данные",
        reply_markup=markup
    )
    await state.set_state(PostAnketaStates.get_info_about_place)


@router.callback_query(PostAnketaStates.get_info_about_place)
async def choose_area_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "another_area_district":
        search = await state.get_data()
        post = search["post"]
        districts = services.fetch_persons_info(post)
        kb = [[types.InlineKeyboardButton(text=district["name"], callback_data=district["name"])] for district in
              districts]
        kb.append(
            [types.InlineKeyboardButton(text='Выбрать другую должность', callback_data='another_post')]
        )
        markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.answer(
            text="Выберите пожалуйста в каком районе вы хотели-бы рассмотреть работу",
            reply_markup=markup)
        await state.set_state(PostAnketaStates.choose_judgment_area)
        return

    id_district = callback.data

    judgment_place = services.fetch_judgement_place_byid(id_district)

    kb = [[types.InlineKeyboardButton(text="Подать документы на этот участок", callback_data=str(id_district))],
          [types.InlineKeyboardButton(text="Выбрать другой участок", callback_data="another")], ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    data = judgment_place
    await callback.message.answer(
        text=f"""<b>Информация по участку №{id_district}</b>\n
        <b>ФИО мирового судьи:</b> \n{data["fio_judgment"]}
        <b>Телефон:</b> {data["phone"]}
        <b>Район:</b><i>{data["district"]}</i>\n
        """,
        #  <b>Адрес участка:</b> {data["Адрес"]}
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )
    await state.set_state(PostAnketaStates.register_hr_site)


@router.callback_query(PostAnketaStates.register_hr_site)
async def start_instruction(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "another":
        # await state.update_data(district=callback.data)
        search = await state.get_data()
        post = search["post"]
        district = search["district"]

        districts = services.fetch_judgment_places(district, int(post))

        if not districts:
            await callback.message.answer(
                text="Извините, в выбранной области нет доступных участков.")
            return
        kb = [
            [types.InlineKeyboardButton(text=f"Участок №" + str(district["id_judgment"]),
                                        callback_data=str(district["id_judgment"]))] for district in districts
        ]
        kb.append(
            [types.InlineKeyboardButton(text=f"Выбрать другой район поиска", callback_data="another_area_district")]
        )
        markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

        await callback.message.answer(
            text="Выберите пожалуйста в какой участок вы хотите отправить данные?",
            reply_markup=markup
        )
        await state.set_state(PostAnketaStates.get_info_about_place)
        return

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
    await state.set_state(PostAnketaStates.fio_ask)


@router.callback_query(PostAnketaStates.fio_ask)
async def filling_fio(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    id_judgement_place = callback.data
    await state.update_data(id_judgement_place=id_judgement_place)
    await callback.message.answer(
        "Для начала введите свое ФИО"
    )
    await state.set_state(PostAnketaStates.email_ask)


@router.message(PostAnketaStates.email_ask)
async def filling_email(message: types.Message, state: FSMContext, *args, **kwargs):
    fio_person = message.text
    await state.update_data(fio_person=fio_person)
    await message.answer("Теперь вам нужно ввести свой email")
    await state.set_state(PostAnketaStates.start_filling_anket)


# @router.message(PostAnketaStates.email_confirm)
# async def confilling_email(message: types.Message, state: FSMContext, *args, **kwargs):
#     email_person = message.text
#     await state.update_data(email_person=email_person)
#     await state.set_state(PostAnketaStates.start_filling_anket)


@router.message(PostAnketaStates.start_filling_anket)
async def filling_anket(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    email_person = message.text
    await state.update_data(email_person=email_person)
    logging.info(f"FILLING ANKET {await state.get_data()}")

    data = await state.get_data()
    id_judgement_place = data["id_judgement_place"]
    # print(await state.get_data())
    # judgment_place = services.fetch_persons_info(filters="filterByFormula={Участок}=" + id_judgement_place)

    # data = judgment_place[0]['fields']

    await message.answer(
        text="Спасибо! После заполнения анкеты, вам необходимо заполнить следующие документы:"
    )

    documents = [
        FSInputFile(directory_path + "/pattern_documents/Анкета.docx"),
        FSInputFile(directory_path + "/pattern_documents/Заявка на секретаря суда.doc"),
        FSInputFile(directory_path + "/pattern_documents/Заявка на секретаря суд. заседания.doc"),
        FSInputFile(directory_path + "/pattern_documents/Список документов на конкурс.doc"),
    ]
    media_docs = []
    for document_to_send in documents:
        media_docs.append(
            types.InputMediaDocument(media=document_to_send)
        )

    chatActionSender = ChatActionSender(
        bot=bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )

    async with chatActionSender as action:
        await bot.send_media_group(message.chat.id, media=media_docs)

    kb = [
        [types.InlineKeyboardButton(text="Я отправил документы ответственному", callback_data=str(id_judgement_place))]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        text="После заполнение документов, вам необходимо отправить их на почту ответственного по участку:"
        # f"\n<b>ФИО ответственного:</b> {data['Сотрудник, ответственный за участок']}"
        # f"\n<b>Почта ответственного:</b> {data['Почта']}",
             f"\n<b>ФИО ответственного:</b> Дупленский Роман Сергеевич"
             f"\n<b>Почта ответственного:</b> duplenskiy@zakon.gov.spb.ru",
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

    # await state.update_data(email=data["Почта"])
    await state.set_state(PostAnketaStates.user_send_docs)


@router.callback_query(PostAnketaStates.user_send_docs)
async def info_about_tender(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    # Функ создания записи кандидата
    data = await state.get_data()
    logging.info("ВСЕ НА ДАННЫЙ МОМЕНТ  " + str(data))
    user_id = callback.from_user.id
    logging.info(user_id)
    fio = str(data["fio_person"])
    surname = fio.split()[0]
    name = fio.split()[1]
    logging.info("Ф= " + surname + " N = " + name)

    services.post_candidate(name, surname, data["email_person"], user_id)

    kb = [
        [types.InlineKeyboardButton(text="Проверить статус заявки", callback_data="data")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await callback.message.answer(
        text="""Отлично!\n 
        Ваша заявка будет рассмотрена в течении трех рабочих дней. Нажмите кнопку, чтобы получить обновленный статус вашей заявки.\n
        """,
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.user_waiting_anket)


@router.callback_query(PostAnketaStates.user_waiting_anket)
async def waiting_for_info(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    kb = [
        [types.InlineKeyboardButton(text="Проверить статус заявки", callback_data="data")]
    ]
    kb2 = [
        [types.InlineKeyboardButton(text="Перейти к подаче документов", callback_data="data")]
    ]
    kb_not_access = [
        [types.InlineKeyboardButton(text="Я отправил документы повторно", callback_data="data")]
    ]
    user_id = callback.from_user.id
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    markup2 = types.InlineKeyboardMarkup(inline_keyboard=kb2)
    markup3 = types.InlineKeyboardMarkup(inline_keyboard=kb_not_access)

    data = services.fetch_candidate_status(user_id)
    status = data["status"]
    # services.fetch_persons_info(filters="filterByFormula={Участок}=")
    # здесь будет сервис о доставлении статуса

    if (status == "not_read"):
        await callback.message.answer(
            text="""Статус вашей заявки: Не просмотрено.\n
        Ваши документы проверяются инспектором. Проверьте статус проверки позже. 
        """,
            reply_markup=markup)

    if (status == "not_access"):
        await callback.message.answer(
            text="""Статус вашей заявки: Не были получены документы.\n
            Документы не были посланы или была выявлена ошибка. Пожалуйста отправьте повторно.
            """,
            reply_markup=markup3)
        services.resend_document_status(callback.from_user.id)

    if (status == "access"):
        await callback.message.answer(
            text="""Статус вашей заявки: Принято.\n
        Теперь вы можете начать процесс поступления на гос службу.
        """,
            reply_markup=markup2)
        await state.set_state(PostAnketaStates.user_collected_all_docs)
        return


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
        FSInputFile(directory_path + "/hiring_docs/Заявление на прием.pdf"),
        FSInputFile(directory_path + "/hiring_docs/Список док-ов на прием.doc")
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
        "Отлично. \nТеперь вам необходимо позвонить специалисту по заполнению справки БК и направить вашу справку на проверку"
    )

