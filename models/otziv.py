class Otziv:
    def __init__(self):
        self.flag = None
        self.screen = None
        self.situation = None
        self.phone = None
        self.username = None
        self.name = None
        self.save_path = None

    async def set_flag(self, flag: bool):
        self.flag = flag

    async def get_flag(self) -> bool:
        return self.flag

    async def set_screen(self, screen: str):
        self.screen = screen

    async def set_situation(self, situation: str):
        self.situation = situation

    async def set_phone(self, phone: str):
        self.phone = phone

    async def set_user_username(self, username: str):
        self.username = username

    async def set_name(self, name: str):
        self.name = name

    async def set_save_path(self, path: str):
        self.save_path = path

    async def get_save_path(self) -> str:
        return self.save_path

    async def get_model(self, flag: bool):
        if flag:
            return {
                "values": [
                    [self.username, self.name, self.phone, self.screen]
                ]
            }
        else:
            return {
                "values": [
                    [self.username, self.name, self.phone, self.situation]
                ]
            }
