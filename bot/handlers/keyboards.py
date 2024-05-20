from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔥ПРОДОЛЖИТЬ🔥', callback_data='start_next')
    return builder.as_markup()

def callback_first_message():
    builder = InlineKeyboardBuilder()
    builder.button(text='Товар супер✅', callback_data='super')
    builder.button(text='Остались вопросы❓', callback_data='bad')
    return builder.as_markup()

def callback_good_opinion():
    keyboard = [
        [
            InlineKeyboardButton(text='Оставил(а) отзыв✅', callback_data='good_otziv'),
            InlineKeyboardButton(text='Не оставил(а) отзыв❌', callback_data='bad_otziv')
        ]
    ]
    builder = InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
    return builder

def callback_bad_opinion():
    builder = InlineKeyboardMarkup()
    builder.add(InlineKeyboardButton(text='Да', callback_data='problem_yes'))
    builder.add(InlineKeyboardButton(text='Нет', callback_data='problem_no'))
    return builder

def callback_bad_otziv():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🤝Перейти к отправке данных🤝', callback_data='next_good'))
    return builder.as_markup()

def after_situation_kbd():
    keyboard = [
        [KeyboardButton(text='👉Далее👈')]
    ]
    builder = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    return builder

def share_contact_kbd():
    keyboard = [
        [KeyboardButton(text='Поделиться контактом☎', request_contact=True)]
    ]
    builder = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return builder

def okey_kbd():
    button = KeyboardButton(text='OK')
    builder = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return builder


