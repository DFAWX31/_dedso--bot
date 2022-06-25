import pathlib

from numpy import full
import settings
import discord
from discord.ext import bridge

def get_files(directory:pathlib.Path) -> list:
	list_of_files = (p for p in directory.iterdir() if p.stem not in ("__init__", "__pycache__"))

	return_list = list()

	for file in list_of_files:
		if file.is_dir():
			return_list.extend(get_files(file))
		else:
			return_list.append(file)

	return return_list

async def _load_cogs(bot):
	cogs_dir = pathlib.Path(__file__).parent.joinpath("cogs")
	paths = get_files(cogs_dir)

	for path in paths:
		trim = str(path).replace(str(cogs_dir), "")
		trim = trim.replace(".py", "")
		main_path = "cogs" + trim.replace("\\", ".")
		bot.load_extension(main_path)

async def create_app():
	intents = discord.Intents.default()
	intents.message_content = True

	bot = bridge.Bot(
		command_prefix=settings.bot.prefix , intents = intents, debig_guilds = [settings.bot.guild]
	)

	await _load_cogs(bot)
	return bot
