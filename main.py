from dotenv import load_dotenv

load_dotenv('env')

from core.bot import HyphendBot
from core.config import Config

config = Config.from_environment()
bot = HyphendBot(config)

bot.run(config.token)