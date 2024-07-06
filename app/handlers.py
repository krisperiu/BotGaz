import aiogram

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database.requests as rq
import app.keyboards as kb 

import os
from dotenv import load_dotenv
load_dotenv()

router=Router()

last_bot_message_id = None


class Report (StatesGroup):
    state_number = State()
    appearance = State()
    cl_interior = State()
    cl_seat = State()
    cl_handles = State()
    seat_integrity = State()
    checklist = State()
    portfolio = State()
    seat_belts = State()
    drivers_appearance = State()
    behaviour = State()
    briefing = State()
    temperature = State()
    comment = State()
    ranked = State()
    photo = State()
    photo_question = State()

class ModerComment(StatesGroup):
    comment = State()

class Moder(StatesGroup):
    tg_id = State()

async def get_user_answer(message: Message):
    if message.text.lower() in ['выполнено', 'не выполнено']:
        return message.text.lower()
    else:
        return None

@router.message(CommandStart())
async def cmd_start(message: Message):
    check = await rq.is_admin(message.from_user.id)
    if check:
        if check.level == 2:
            await message.answer('Добрый день! В меню ниже вы можете просмотреть оценки транспорта и посмотреть список модераторов.', reply_markup = kb.start_admin)
        else:
            await message.answer('Добрый день! В меню ниже вы можете просмотреть оценки транспорта.', reply_markup = kb.start_moderator)
    else:
        await message.answer('Добрый день! В меню ниже вы можете перейти к своим оценкам транспорта или оставить новую.', reply_markup = kb.start_user)

        

@router.callback_query(F.data == 'new_report')
async def new_report_1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Report.state_number)
    await callback.message.edit_text('Введите государственный номер автобуса в виде "Х000ХХ00" или "Х000ХХ000".')

@router.message(Report.state_number)
async def new_report_2(message: Message, state: FSMContext):
    bus = await rq.get_bus_by_state_number(message.text)
    if bus:
        await state.update_data(state_number = message.text)
        await state.set_state(Report.appearance)
        await message.answer('Чистота, отсутствие следов влияния внешних факторов на кузов ТС.\nВыберите вариант ответа внизу.', reply_markup = kb.question)
    else:
        await message.answer(f'На автобус с госномером {message.text} нельзя оставить оценку.', reply_markup = kb.start_user)
        await state.clear()
    
@router.message(Report.appearance)
async def new_report_3(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(appearance = message.text)
    await state.set_state(Report.cl_interior)
    await message.answer('Чистота салона.\nВыберите вариант ответа внизу.')

@router.message(Report.cl_interior)
async def new_report_4(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(cl_interior = message.text)
    await state.set_state(Report.cl_seat)
    await message.answer('Чистота сидений.\nВыберите вариант ответа внизу.')

@router.message(Report.cl_seat)
async def new_report_5(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(cl_seat = message.text)
    await state.set_state(Report.cl_handles)
    await message.answer('Чистота ручек.\nВыберите вариант ответа внизу.')
        
@router.message(Report.cl_handles)
async def new_report_6(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(cl_handles = message.text)
    await state.set_state(Report.seat_integrity)
    await message.answer('Целостность сидений.\nВыберите вариант ответа внизу.')

@router.message(Report.seat_integrity)
async def new_report_7(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(seat_integrity = message.text)
    await state.set_state(Report.checklist)
    await message.answer('Наличие в салоне памятки пассажира.\nВыберите вариант ответа внизу.')

@router.message(Report.checklist)
async def new_report_8(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(checklist = message.text)
    await state.set_state(Report.portfolio)
    await message.answer('Наличие в салоне портфолио водителя.\nВыберите вариант ответа внизу.')

@router.message(Report.portfolio)
async def new_report_9(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(portfolio = message.text)
    await state.set_state(Report.seat_belts)
    await message.answer('Наличие в исправном состоянии ремней безопасности.\nВыберите вариант ответа внизу.')

@router.message(Report.seat_belts)
async def new_report_10(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(seat_belts = message.text)
    await state.set_state(Report.drivers_appearance)
    await message.answer('Опрятный внешний вид водителя.\nВыберите вариант ответа внизу.')

@router.message(Report.drivers_appearance)
async def new_report_11(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(drivers_appearance = message.text)
    await state.set_state(Report.behaviour)
    await message.answer('Доброжелательное поведение водителя.\nВыберите вариант ответа внизу.')

@router.message(Report.behaviour)
async def new_report_12(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(behaviour = message.text)
    await state.set_state(Report.briefing)
    await message.answer('Проведен ли инструктаж водителем (аудио ассистентом) перед началом поездки.\nВыберите вариант ответа внизу.')

@router.message(Report.briefing)
async def new_report_13(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(briefing = message.text)
    await state.set_state(Report.temperature)
    await message.answer('Комфортная температура в салоне (работающий кондиционер летом/работающая печь зимой).\nВыберите вариант ответа внизу.')

@router.message(Report.temperature)
async def new_report_14(message: Message, state: FSMContext):
    user_answer = await get_user_answer(message)
    if user_answer is None:
        await message.answer('Пожалуйста, выберите один из вариантов ответа: "Выполнено" или "Не выполнено".')
        return
    await state.update_data(temperature = message.text)
    await state.set_state(Report.comment)
    await message.answer('Оставьте комментарий.', reply_markup= ReplyKeyboardRemove())

@router.message(Report.comment)
async def new_report_15(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(Report.photo_question)
    await message.answer('Хотите оставить фото?', reply_markup=kb.question_photo)

@router.message(Report.photo_question)
async def handle_photo_question(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        await state.set_state(Report.photo)
        await message.answer('Пожалуйста, загрузите фото. Когда закончите, отправьте "Готово".', reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(Report.ranked)
        await message.answer('Оставьте оценку от 1 до 5.', reply_markup=ReplyKeyboardRemove())

@router.message(Report.photo, F.photo | F.text)
async def handle_photo(message: Message, state: FSMContext):
    if message.content_type == F.photo and message.photo:
        photo = message.photo[-1]
        photo_id = photo.file_id
        data = await state.get_data()
        photos = data.get('photos', [])
        photos.append(photo_id)
        await state.update_data(photos=photos)
        await message.answer('Фото добавлено. Вы можете загрузить ещё фото или отправить "Готово", чтобы продолжить.')
    elif message.content_type == F.text and message.text.lower() == 'готово':
        await state.set_state(Report.ranked)
        await message.answer('Оставьте оценку от 1 до 5.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста, загрузите фото или отправьте "Готово", чтобы продолжить.')

@router.message(Report.ranked)
async def new_report_16(message: Message, state: FSMContext):
    try:
        ranked = int(message.text)
        if ranked < 1 or ranked > 5:
            raise ValueError()
        
        await state.update_data(ranked=ranked)
        data = await state.get_data()
        photos = data.get('photos', [])
        await rq.ins_report(
            message.from_user.id,
            message.from_user.username,
            data["state_number"],
            data["appearance"],
            data["cl_interior"],
            data["cl_seat"],
            data["cl_handles"],
            data["seat_integrity"],
            data["checklist"],
            data["portfolio"],
            data["seat_belts"],
            data["drivers_appearance"],
            data["behaviour"],
            data["briefing"],
            data["temperature"],
            data["comment"],
            int(data["ranked"]),
            photos
        )
        await message.answer('Спасибо, ваша оценка сохранена.', reply_markup=kb.start_user)
        await state.clear()
        
    except ValueError:
        await message.answer("Некорректная оценка. Пожалуйста, введите оценку еще раз.")

@router.callback_query(F.data == 'my_reports')
async def my_reports(callback: CallbackQuery):
    global last_bot_message_id
    reps = await rq.check_reps(callback.from_user.id)
    if reps:
        sent_message = await callback.message.edit_text('Выберите оценку из списка ниже.', reply_markup= await kb.user_reports(reps))
        last_bot_message_id = sent_message.message_id
    else:
        await callback.message.edit_text('Вы не оставляли оценки.')
        await callback.message.answer('В меню ниже вы можете перейти к своим оценкам или оставить новую.', reply_markup = kb.start_user)

@router.callback_query(F.data.startswith('report_'))
async def report_n(callback: CallbackQuery, state: FSMContext):
    global last_bot_message_id
    parts = callback.data.split('_')
    report_id = int(parts[1])
    type = int(parts[2])
    rep = await rq.get_report_by_id(report_id)
    check = await rq.is_admin(callback.from_user.id)
    if check:
        await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_bot_message_id)
        await state.update_data(report_id = report_id)
        report_text = (
            f'Оценка №: {rep.id}\n'
            f'Госномер автобуса: {rep.state_number}\n'
            f'Дата: {rep.date}\n'
            f'Пользователь: @{rep.name}\n'
            f'Внешний вид тс: {rep.appearance}\n'
            f'Чистота салона: {rep.cl_interior}\n'
            f'Чистота сидений: {rep.cl_seat}\n'
            f'Чистота ручек: {rep.cl_handles}\n'
            f'Целостность сидений: {rep.seat_integrity}\n'
            f'Наличие в салоне памятки пассажира: {rep.checklist}\n'
            f'Наличие в салоне портфолио водителя: {rep.portfolio}\n'
            f'Наличие в исправном состоянии ремней безопасности: {rep.seat_belts}\n'
            f'Опрятный внешний вид водителя: {rep.drivers_appearance}\n'
            f'Доброжелательное поведение водителя: {rep.behaviour}\n'
            f'Проведен ли инструктаж водителем (аудио ассистентом) перед началом поездки: {rep.briefing}\n'
            f'Комфортная температура в салоне (работающий кондиционер летом/работающая печь зимой): {rep.temperature}\n'
            f'Комментарии пассажира: {rep.comment}\n'
            f'Оценка пассажира: {rep.ranked}\n'
            f'Комментарий модератора: {rep.comment_moder}'
        )

        if rep.photos:
            for idx, photo in enumerate(rep.photos, start=1):
                await callback.message.answer_photo(photo.photo_id, caption=f'Оценка №: {rep.id}\n'
                                                    f'Фото {idx}')

        await callback.message.answer(
            report_text,
            reply_markup=await kb.report_edit_moder(type)
        )
    else:  
        await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_bot_message_id)
        if rep.status == 0:
            status = 'На рассмотрении'
        else: 
            status = 'Рассмотрена'
        text_message = (
            f'Оценка №: {rep.id}\n'
            f'Оценка на автобус: {rep.state_number}\n'
            f'Дата: {rep.date}\n'
            f'Статус: {status}\n'
            f'Комментарий специалиста: {rep.comment_moder}\n'
        )
        if rep.photos:
            for idx, photo in enumerate(rep.photos, start=1):
                await callback.message.answer_photo(photo.photo_id, caption=f'Оценка №: {rep.id}\n'
                                                    f'Фото {idx}')
 
        await callback.message.answer(
            text_message,
            reply_markup = kb.back_my_reports
        )

@router.callback_query(F.data.startswith('page_'))
async def paginate_reports(callback: CallbackQuery):
    parts = callback.data.split('_')
    page = int(parts[1])
    type = int(parts[2])
    check = await rq.is_admin(callback.from_user.id)
    if check:
        reps = await rq.check_moder_reps(type)
    else:
        reps = await rq.check_reps(callback.from_user.id)
    keyboard = await kb.user_reports(reps, type, page)
    await callback.message.edit_text('Выберите оценку из списка ниже.', reply_markup=keyboard)

@router.callback_query(F.data == 'back_to_start')
async def back_to_start(callback: CallbackQuery):
    check = await rq.is_admin(callback.from_user.id)
    if check:
        if check.level == 2:
            await callback.message.edit_text('Добрый день! В меню ниже вы можете просмотреть оценки транспорта и посмотреть список модераторов.', reply_markup = kb.start_admin)
        else:
            await callback.message.edit_text('Добрый день! В меню ниже вы можете просмотреть оценки транспорта.', reply_markup = kb.start_moderator)
    else:
        await callback.message.edit_text('Добрый день! В меню ниже вы можете перейти к своим оценкам транспорта или оставить новую.', reply_markup = kb.start_user)

@router.callback_query(F.data == 'check_reports')
async def check_reports(callback: CallbackQuery):
    await callback.message.edit_text('Выберите, какие оценки вы хотите посмотреть',reply_markup=kb.reports_moder)

@router.callback_query(F.data == 'check_new_reports')
async def check_new_reports(callback: CallbackQuery):
    global last_bot_message_id
    reps = await rq.check_moder_reps(0)
    if reps:
        sent_message = await callback.message.edit_text('Выберите оценку из списка ниже.', reply_markup= await kb.user_reports(reps))
        last_bot_message_id = sent_message.message_id
    else:
        await callback.message.edit_text('Новых оценок нет.')
        await callback.message.answer('Выберите, какие оценки вы хотите посмотреть',reply_markup=kb.reports_moder)

@router.callback_query(F.data == 'edit_new_report')
async def edit_new_report(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ModerComment.comment)
    await callback.message.edit_text('Оставьте комментарий для пользователя.')

@router.message(ModerComment.comment)
async def edit_new_report2(message: Message, state: FSMContext):
    from run import bot
    await state.update_data(comment = message.text)
    data_com = await state.get_data()
    await rq.update_comment_moder(data_com['report_id'], data_com['comment'])
    rep = await rq.get_report_by_id(data_com['report_id'])
    await bot.send_message(chat_id=rep.tg_id, text=f'Новый комментарий от модератора по оценке №{rep.id}')
    await message.answer('Спасибо, комментарий сохранен.')
    await message.answer('Выберите, какие оценки вы хотите посмотреть.', reply_markup = kb.reports_moder)
    await state.clear()

@router.callback_query(F.data == 'check_old_reports')
async def check_old_reports(callback: CallbackQuery):
    global last_bot_message_id
    reps = await rq.check_moder_reps(1)
    if reps:
        sent_message = await callback.message.edit_text('Выберите оценку из списка ниже.', reply_markup= await kb.user_reports(reps,1))
        last_bot_message_id = sent_message.message_id
    else:
        await callback.message.edit_text('Рассмотренных оценок нет.')
        await callback.message.answer('Выберите, какие оценки вы хотите посмотреть',reply_markup=kb.reports_moder)

@router.callback_query(F.data == 'check_moderators')
async def check_moders(callback: CallbackQuery):
    moders = await rq.is_moder(1)
    if moders:
        await callback.message.edit_text('Выберите модератора из списка ниже.', reply_markup= await kb.moders(moders))
    else:
        await callback.message.edit_text('Модераторы не назначены.', reply_markup=kb.if_no_moders)

@router.callback_query(F.data == 'ins_new_moder')
async def ins_new_moder(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Moder.tg_id)
    await callback.message.edit_text('Отправьте тг id пользователя.')

@router.message(Moder.tg_id)
async def ins_moder_byId(message: Message, state: FSMContext):
    try:
        tg_id = int(message.text)
        check = await rq.is_admin(tg_id)
        if check:
            await message.answer(f'Пользователь с айди {tg_id} уже является администратором.')
        else:
            await rq.ins_moder(tg_id)
            await message.answer(f'Модератор с айди {tg_id} назначен.')
        await message.answer('Добрый день! В меню ниже вы можете просмотреть оценки транспорта и посмотреть список модераторов.', reply_markup = kb.start_admin)    
        await state.clear()
    except ValueError:
        await message.answer("Некорректный id. Пожалуйста, введите id еще раз.")

@router.callback_query(F.data.startswith('pageModers_'))
async def paginate_moders(callback: CallbackQuery):
    page_m = int(callback.data.replace('pageModers_', ''))
    moders = await rq.is_moder(1)
    keyboard = await kb.moders(moders, page_m)
    await callback.message.edit_text('Выберите модератора.', reply_markup = keyboard)

@router.callback_query(F.data.startswith('moder_'))
async def moder_n(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    moder_id = int(callback.data.replace('moder_',''))
    moder = await rq.admin_by_id(moder_id)
    await state.update_data(id = moder_id)
    await callback.message.edit_text(f'Tg id: {moder.tg_id}\nУровень: {moder.level}', reply_markup = kb.edit_moder)

@router.callback_query(F.data == 'delete_moder')
async def delete_moder(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data() 
    await callback.message.edit_text('Вы уверены, что хотите удалить модератора?',reply_markup=await kb.approve(data['id']))
    data1 = await state.get_data()

@router.callback_query(F.data == 'delete_approve')
async def delete_approve(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.delete_moder(int(data['id']))
    await state.clear()
    await callback.message.edit_text('Модератор удален')
    await callback.message.answer('Добрый день! В меню ниже вы можете просмотреть оценки транспорта и посмотреть список модераторов.', reply_markup = kb.start_admin)