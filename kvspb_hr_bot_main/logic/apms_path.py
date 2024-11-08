
from aiogram import Router, types, Bot, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from urllib3.exceptions import RequestError

import texts
import services
from services import get_unique_data_by_field
import requests

router = Router()


booking_data = {}

class PostAnketaStates(StatesGroup):
    choose_district = State()
    choose_judgment_area = State()
    get_info_about_place = State()
    start_filling_anket = State()
    user_send_docs = State()
    user_collected_all_docs = State()


class BookingVisitor(StatesGroup):
    choose_time_visit = State()
    accept_time_visit = State()
    enter_fio = State()
    enter_id_judge = State()


@router.callback_query(lambda msg: msg.data == texts.administration)
async def choose_post_handler(callback: types.CallbackQuery, state: FSMContext):

    posts = get_unique_data_by_field("Должность", services.fetch_available_posts)
    print("38",posts)

    kb = [[types.InlineKeyboardButton(text=post, callback_data=post)] for post in posts]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)


    await callback.message.answer(
        text="Выберите пожалуйста интересущую вас должность из списка ниже",
        reply_markup=markup
    )

    await state.set_state(PostAnketaStates.choose_district)


@router.callback_query(PostAnketaStates.choose_district)
async def choose_district_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(post=callback.data)
    # print(f"Вабрана следующая должность:", callback.data, f"Поиска: {search}")
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
    print("75",districts)

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
    await state.set_state(PostAnketaStates.start_filling_anket)


@router.callback_query(PostAnketaStates.start_filling_anket)
async def filling_anket(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    id_judgement_place = callback.data
    print('122', id_judgement_place)

    await state.update_data(id_judgement_place=id_judgement_place)

    judgment_place = services.fetch_persons_info(filters="{Участок} = " + id_judgement_place)

    data = judgment_place[0]['fields']
    print(await state.get_data())

    await callback.message.answer(
        text="Спасибо, что выбрали этот участок. Для того чтобы вам подать анкету, необходимо заполнить следующие документы:"
    )

    documents = [
        FSInputFile("logic/pattern_documents/Анкета.rtf"),
        FSInputFile("logic/pattern_documents/Заявление на конкурс К.Р.с.с.doc"),
        FSInputFile("logic/pattern_documents/Заявление на конкурс К.Р.с.с.з.doc"),
        FSInputFile("logic/pattern_documents/список на прием через конкурс.doc"),
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
    print(await state.get_data())

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
async def choose_time_visit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

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
        FSInputFile("logic/hiring_docs/прием на должность.doc"),
        FSInputFile("logic/hiring_docs/список на прием.doc")
    ]
    media_docs = []
    for document_to_send in documents:
        media_docs.append(
            types.InputMediaDocument(media=document_to_send)
        )
    await callback.message.answer(
        text="Документы, который нужно заполнить для трудоустройтва",
    )
    await bot.send_media_group(callback.message.chat.id, media=media_docs)

    await callback.message.answer(
        "Также обращаем ваше внимание на заполнение справки о доходах и расходах. Перед заполнением ознакомьтесь с инструкцией,"
        "которая доступна по ссылке: https://disk.yandex.ru/d/HRKduVqyksUlvg",
        reply_markup=markup,

    )

    await state.set_state(BookingVisitor.choose_time_visit)


@router.callback_query(BookingVisitor.choose_time_visit)
async def choose_time_visit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):

    state_data = await state.get_data()


    print("223",state_data)
    try:
        response = requests.get(
            f"http://backend:8000/api/free-time-windows?email={state_data['email']}"
        )

        if response.json() == []:
            raise ValueError

        kb = [[types.InlineKeyboardButton(text=f"{date['date']} (с {date['time_start']} до {date['time_end']})", callback_data=f"{date['id']}")] for date in response.json()]
        markup = types.InlineKeyboardMarkup(inline_keyboard=kb)

        await callback.message.answer(
            "Выберите доступные даты и время для посещения",
            reply_markup=markup
        )
        await state.set_state(BookingVisitor.accept_time_visit)

    except ValueError:
        print("ValueError")
        await callback.message.answer("Приносим свои извинения, но на данный момент, выбрать время окон нельзя."
                                      "Попробуйте отправить запрос позднее")
        await state.set_state(BookingVisitor.choose_time_visit)
    except Exception as e:
        print("Exception", e)
        await callback.message.answer("Приносим свои извинения, но входе обработки данных, возникла ошибка")
        await state.set_state(BookingVisitor.choose_time_visit)


@router.callback_query(BookingVisitor.accept_time_visit)
async def choose_time_visit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    time_ticket = callback.data
    await state.update_data(time_ticket=time_ticket)
    await callback.message.answer("Отлично. Теперь введите ваше ФИО")
    await state.set_state(BookingVisitor.enter_fio)


@router.message(F.text,BookingVisitor.enter_fio)
async def enter_fio(message: types.Message, state: FSMContext, bot: Bot):
    fio = message.text

    collected_data = await state.get_data()
    print("254", collected_data)

    try:
        response = requests.post(
            f"http://backend:8000/api/take-time-windows",
            data={
                "person_data": fio,
                "telegram_nickname": message.from_user.username,
                "id_judgement_place": int(collected_data["id_judgement_place"]),
                "taken_time": collected_data["time_ticket"],
            }
        )
        print(response)

        if response.status_code in (404, 400, ):
            raise Exception

        await message.answer("Ваша очередь оформлена на выбранное вами время.\n\n"
                             "Ждем вас по адресу:\n"
                             "191060, г Санкт-Петербург,проезд Смольный, д.1, лит.Б, 6 подъезд")
    except Exception as e:
        print(e)
        await message.answer("Приносим свои извинения, но входе обработки данных, возникла ошибка")

