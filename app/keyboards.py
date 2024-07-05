from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq

start_user = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Оставить жалобу',callback_data='new_report')],
    [InlineKeyboardButton(text='Мои жалобы',callback_data='my_reports')]
])

start_moderator = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр жалоб', callback_data='check_reports')]
])

start_admin = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр жалоб', callback_data='check_reports')],
    [InlineKeyboardButton(text='Модераторы', callback_data='check_moderators')]
])

back_to_start = InlineKeyboardButton(text='На главную', callback_data='back_to_start')

back_my_reports = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='my_reports')]
])

question = ReplyKeyboardMarkup (keyboard=[
    [KeyboardButton(text = 'Выполнено'),
    KeyboardButton(text = 'Не выполнено')]
], resize_keyboard= True, input_field_placeholder='Выберите из вариантов снизу')

async def user_reports(reps, page=1):
    inline_keyboard = []
    ITEMS_PER_PAGE = 5
    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    paginated_reps = reps[start_index:end_index]
    total_pages = (len(reps) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    for report in paginated_reps:
        button_text = f'Оценка на автобус с госномером: {report.state_number}'
        callback_data = f'report_{report.id}'
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        inline_keyboard.append([button])
    
    navigation_buttons = []
    if start_index > 0:
        navigation_buttons.append(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'page_{page-1}'))
    
    page_counter = InlineKeyboardButton(text=f'Страница {page}/{total_pages}', callback_data='page_counter', callback_disabled=True)
    navigation_buttons.append(page_counter)

    if end_index < len(reps):
        navigation_buttons.append(InlineKeyboardButton(text='Вперед ➡️', callback_data=f'page_{page+1}'))
    
    if navigation_buttons:
        inline_keyboard.append(navigation_buttons)

    inline_keyboard.append([back_to_start])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard

reports_moder = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр нерассмотренных жалоб', callback_data='check_new_reports')],
    [InlineKeyboardButton(text='Просмотр рассмотренных жалоб', callback_data='check_old_reports')],
    [back_to_start]
])

report_edit_moder = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Рассмотреть жалобу', callback_data='edit_new_report')],
    [InlineKeyboardButton(text='Назад', callback_data='check_new_reports')]
])

ins_new_moder = InlineKeyboardButton(text='Назначить модератора', callback_data='ins_new_moder')

if_no_moders = InlineKeyboardMarkup (inline_keyboard=[[ins_new_moder], [back_to_start]])

async def moders(moders, page=1):
    inline_keyboard = []
    ITEMS_PER_PAGE = 5
    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    paginated_moders = moders[start_index:end_index]
    total_pages = (len(moders) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    for moder in paginated_moders:
        button_text = f'Модератор с тг id: {moder.tg_id}'
        callback_data = f'moder_{moder.id}'
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        inline_keyboard.append([button])
    
    navigation_buttons = []
    if start_index > 0:
        navigation_buttons.append(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'pageModers_{page-1}'))
    
    page_counter = InlineKeyboardButton(text=f'Страница {page}/{total_pages}', callback_data='page_counter', callback_disabled=True)
    navigation_buttons.append(page_counter)

    if end_index < len(moders):
        navigation_buttons.append(InlineKeyboardButton(text='Вперед ➡️', callback_data=f'pageModers_{page+1}'))
    
    if navigation_buttons:
        inline_keyboard.append(navigation_buttons)

    inline_keyboard.append([back_to_start])
    inline_keyboard.append([ins_new_moder])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard
edit_moder = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Удалить модератора', callback_data='delete_moder')],
    [InlineKeyboardButton(text='Назад', callback_data='check_moderators')],
    [back_to_start]
])
async def approve(id):
    inline_keyboard = [[InlineKeyboardButton(text='Да', callback_data='delete_approve')],
    [InlineKeyboardButton(text='Нет', callback_data=f'moder_{id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard