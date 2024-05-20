from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    start = State()
    save_situation = State()
    enter_photo = State()
    enter_contact = State()
    enter_name = State()
    save_in_sheets = State()
    save_in_sheets_situation = State()
