from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ContentType, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from bot.utils.state_management import UserState
from bot.services.user_storage import user_storage
from bot.services.google_sheets import upload_photo_to_drive, append_to_sheet
from bot.handlers.keyboards import start_keyboard, callback_first_message, callback_good_opinion, callback_bad_opinion, \
    callback_bad_otziv, after_situation_kbd, share_contact_kbd, okey_kbd
import os
router = Router()

sheet_id = "1Ay3R8wGXQ51Qv6JjwvXwR8ATO8m3UFu57W0dwqT-grc"

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state(UserState.start)
    await message.answer('<b><i>Здравствуйте!😊</i></b>', reply_markup=ReplyKeyboardRemove(), parse_mode='html')
    await message.answer(
        'Cпасибо за то что приобрели нашу продукцию.🙏\n'
        'Рады приветствовать вас в сервисе поддержки клиентов. '
        'Для продолжения нажмите кнопку 👉<b>«ПРОДОЛЖИТЬ»</b>👈',
        reply_markup=start_keyboard(), parse_mode='html'
    )

@router.callback_query(StateFilter(UserState.start))
async def blagodar_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_next':
        await user_storage.add_user(call.from_user.id)
        await call.message.answer(
            "Нам важно знать мнение покупателей о нашей продукции, поэтому мы просим вас поделиться впечатлением о товаре🤔",
            reply_markup=callback_first_message()
        )

    elif call.data == 'super':
        await user_storage.user_set_flag(call.from_user.id, True)
        await call.message.answer(
            'Мы очень рады, что вам понравился наш товар👌\nУ вас есть возможность '
            'воспользоваться выгодным предложением и получить бонус🎁'
            '\nДля этого необходимо оставить <b>отзыв</b>📝\n'
            '⬇Нажмите на одну из кнопок⬇',
            reply_markup=callback_good_opinion(), parse_mode='html'
        )

    elif call.data == 'good_otziv':
        await call.message.answer('Спасибо вам за то, что вы оставили отзыв👍\nДля получения бонуса '
                                                  'следуйте инструкции:\n'
                                                  '1⃣ Зайдите в личный кабинет WB.\n'
                                                  '2⃣ Откройте раздел <b>"Мои покупки"</b>.\n'
                                                  '3⃣ Убедиетсь в том, что отзыв опубликован и сделайте скриншот '
                                                  'оставленного отзыва.\n'
                                                  '4⃣ Для дальнейших действий нажмите кнопку '
                                                  '<b>"Перейти к отправке данных"</b>📬',
                               reply_markup=callback_bad_otziv(), parse_mode='html')


    if call.data == 'bad_otziv':
        await call.message.answer('Для получения бонуса следуйте инструкции:\n'
                                                     '1⃣ Зайдите в личный кабинет WB.\n'
                                                     '2⃣ Откройте раздел <b>"Мои покупки"</b>.\n'
                                                     '3⃣ Выберите наш товар и оставьте <b>положительный отзыв</b>.\n'
                                                     '4⃣ Дождитесь публикации отзыва и сделайте скриншот '
                                                     'оставленного отзыва из раздела <b>"Мои покупки"</b> в '
                                                     'личном кабинете.\n'
                                                     '5⃣ Для дальнейших действий нажмите кнопку '
                                                     '<b>"Перейти к отправке данных"</b>📬',
                               reply_markup=callback_bad_otziv(), parse_mode='html')

    elif call.data == 'bad':
        await user_storage.user_set_flag(call.from_user.id, False)
        await call.message.answer(
            'В случае возникновения проблем, подробно опишите вашу проблему📝',
        )
        await state.set_state(UserState.save_situation)

    elif call.data == 'next_good':
        await call.message.answer('Прикрепите скриншот отзыва📱')
        await state.set_state(UserState.enter_photo)

@router.message(UserState.save_situation)
async def after_situation(message: types.Message, state: FSMContext):
    if message.text is None:
        builder = ReplyKeyboardMarkup(resize_keyboard=True)
        builder.add(KeyboardButton(text='OK'))
        await state.set_state(UserState.start)
        await message.answer('⛔В данное поле можно ввести только символы с клавиатуры⛔', reply_markup=builder)
        return
    await user_storage.user_set_situation(message.from_user.id, message.text)
    await message.answer('Большое спасибо за отзыв😇', reply_markup=after_situation_kbd())
    await state.set_state(UserState.enter_contact)

@router.message(UserState.enter_photo, F.content_type == ContentType.PHOTO)
async def instruction1_function(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.PHOTO:
        await message.answer('Фото обрабатывается, пожалуйста подождите🔄')
        save_path = f'photo{message.photo[-1].file_id}.jpg'
        await user_storage.user_set_save_path(message.from_user.id, save_path)
        #await tg_bot.download_file_by_id(message.photo[-1].file_id, save_path)

        file_id = message.photo[-1].file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        await message.bot.download_file(file_path, save_path)
        # Загружаем фото в Google Drive
        link = await upload_photo_to_drive(save_path)
        await user_storage.user_set_screen(message.from_user.id, link)
        await state.set_state(UserState.enter_contact)
        await message.answer('Обработка завершена✅', reply_markup=okey_kbd())
    else:
        await message.answer('⛔Произошла ошибка, попробуйте, еще раз⛔')

@router.message(UserState.enter_photo, F.content_type != ContentType.PHOTO)
async def instruction1_function1(message: types.Message, state: FSMContext):
    await message.answer('⛔Произошла ошибка, попробуйте, еще раз⛔')

@router.message(UserState.enter_contact)
async def call_get_phoneee(message: types.Message, state: FSMContext):
    save_path = await user_storage.user_get_save_path(message.from_user.id)
    if save_path:
        await message.bot.delete_message(message.from_user.id, message_id=message.message_id)
        os.remove(save_path)
    if not await user_storage.get_user_flag(message.from_user.id):
        if message.text is None:
            builder = ReplyKeyboardMarkup(resize_keyboard=True)
            builder.add(KeyboardButton(text='OK'))
            await state.set_state(UserState.start)
            await message.answer('⛔В данное поле можно ввести только символы с клавиатуры⛔', reply_markup=builder)
            return
    await message.answer(
        'Поделитесь контактом, чтобы наш менеджер мог связаться с вами👨‍💻',
        reply_markup=share_contact_kbd()
    )
    await state.set_state(UserState.enter_name)

@router.message(UserState.enter_name, F.content_type != ContentType.CONTACT)
async def phone_number_except(message: types.Message, state: FSMContext):
    await state.set_state(UserState.enter_contact)
    await message.answer('Вам нужно просто нажать на кнопку снизу', reply_markup=okey_kbd())


@router.message(UserState.enter_name, F.content_type == ContentType.CONTACT)
async def get_phone_mes(message: types.Message, state: FSMContext):
    if message.contact:
        await user_storage.user_set_phone(message.from_user.id, message.contact.phone_number)
        await message.answer('Введите ваше имя для связи✋', reply_markup=ReplyKeyboardRemove())
        if not await user_storage.get_user_flag(message.from_user.id):
            await state.set_state(UserState.save_in_sheets_situation)
        else:
            await state.set_state(UserState.save_in_sheets)
    else:
        await phone_number_except(message, state)

@router.message(UserState.save_in_sheets)
async def save_in_sheets(message: types.Message, state: FSMContext):
    await user_storage.user_set_username(message.from_user.id, message.from_user.username)
    await user_storage.user_set_name(message.from_user.id, message.text)
    data = await user_storage.return_body(message.from_user.id, True)
    await append_to_sheet(sheet_id, data, "Лист1!A1", True)
    await message.answer('Отлично☑\nС вами свяжется наш менеджер для получения бонуса')
    await user_storage.remove_user(message.from_user.id)
    await state.clear()

@router.message(UserState.save_in_sheets_situation)
async def save_in_sheets_situation(message: types.Message, state: FSMContext):
    await user_storage.user_set_username(message.from_user.id, message.from_user.username)
    await user_storage.user_set_name(message.from_user.id, message.text)
    data = await user_storage.return_body(message.from_user.id, False)
    await append_to_sheet(sheet_id, data, "Лист2!A1", False)
    await message.answer('Спасибо, что поделились мнением🙏\nНаш менеджер свяжется с вами в ближайшее время👨‍💻')
    await user_storage.remove_user(message.from_user.id)
    await state.clear()

