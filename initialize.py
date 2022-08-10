from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import ImsBot


_API_TOKEN = "5336663790:AAH1RsdS577--oXpQq1CpL2IDcWh8pOiUpU"
_bot = Bot(token=_API_TOKEN)
# _storage = MemoryStorage()
print("Connecting to Redis...")
_storage = storage = RedisStorage2(host="127.0.0.1", port=6379, db=1)
print("Connected!")
_dp = Dispatcher(_bot, storage=_storage)

bot = ImsBot(_bot, _dp)
