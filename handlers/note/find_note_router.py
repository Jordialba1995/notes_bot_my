from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao import get_notes_by_user
from keyboards_my.note_kb import main_note_kb, find_note_kb, generate_date_keyboard, generate_type_content_keyboard
from utils.utils import send_many_notes


class FindNoteStates(StatesGroup):
    text = State()  # Ожидаем текст для поиска заметок


find_note_router = Router()


@find_note_router.message(F.text == '📋 Просмотр заметок')
async def start_views_noti(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери какие заметки отобразить', reply_markup=find_note_kb())


@find_note_router.message(F.text == '📋 Все заметки')
async def all_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_notes_by_user(user_id=message.from_user.id)
    if all_notes:
        await send_many_notes(all_notes, bot, message.from_user.id)
        await message.answer(f'Все ваши {len(all_notes)} заметок отправлены!', reply_markup=main_note_kb())
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())

# Поиск заметок по дате добавления.
@find_note_router.message(F.text == '📅 По дате добавления')
async def date_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_notes_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('На какой день вам отобразить заметки?',
                             reply_markup=generate_date_keyboard(all_notes))
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())


@find_note_router.callback_query(F.data.startswith('date_note_'))
async def find_note_to_date(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    date_add = call.data.replace('date_note_', '')
    all_notes = await get_notes_by_user(user_id=call.from_user.id, date_add=date_add)
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши {len(all_notes)} заметок на {date_add} отправлены!',
                              reply_markup=main_note_kb())








