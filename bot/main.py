from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
import os
import asyncio
from bot.handlers.messages import router
from bot.utils import UserState, get_redis_connection


env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)
bot_token = os.getenv('token')

tg_bot = Bot(bot_token)
host = os.getenv('REDIS_HOST', 'localhost')
port = int(os.getenv('REDIS_PORT', 6379))
redis_conn = get_redis_connection('localhost', 6379)
storage = RedisStorage(redis_conn)
dp = Dispatcher(storage=storage)
dp.include_router(router)


async def main():
    await redis_conn.flushall()
    await dp.start_polling(tg_bot)

if __name__ == "__main__":
    asyncio.run(main())

