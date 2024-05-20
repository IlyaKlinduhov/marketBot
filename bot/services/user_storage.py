from models.otziv import Otziv
from typing import Dict

class UserStorage:
    def __init__(self):
        self.users: Dict[int, Otziv] = {}

    async def add_user(self, id: int):
        self.users[id] = Otziv()

    async def remove_user(self, id: int):
        if id in self.users:
            del self.users[id]

    async def find_user(self, id: int):
        return self.users.get(id)

    async def get_user_flag(self, id: int):
        user = self.users.get(id)
        if user:
            return await user.get_flag()

    async def user_set_flag(self, id: int, flag: bool):
        user = self.users.get(id)
        if user:
            await user.set_flag(flag)

    async def user_set_screen(self, id: int, screen: str):
        user = self.users.get(id)
        if user:
            await user.set_screen(screen)

    async def user_set_situation(self, id: int, situation: str):
        user = self.users.get(id)
        if user:
            await user.set_situation(situation)

    async def user_set_phone(self, id: int, phone: str):
        user = self.users.get(id)
        if user:
            await user.set_phone(phone)

    async def user_set_username(self, id: int, username: str):
        user = self.users.get(id)
        if user:
            await user.set_user_username(username)

    async def user_set_name(self, id: int, name: str):
        user = self.users.get(id)
        if user:
            await user.set_name(name)

    async def user_set_save_path(self, id: int, path: str):
        user = self.users.get(id)
        if user:
            await user.set_save_path(path)

    async def user_get_save_path(self, id: int):
        user = self.users.get(id)
        if user:
            return await user.get_save_path()

    async def return_body(self, id: int, flag: bool):
        user = self.users.get(id)
        if user:
            return await user.get_model(flag)

user_storage = UserStorage()
