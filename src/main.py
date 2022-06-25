import asyncio

from dotenv import load_dotenv

async def main() -> None:
	import bot
	import settings

	bot = await bot.create_app()

	await bot.start(token=settings.bot.token)

if __name__ == "__main__":
	load_dotenv()
	asyncio.run(main())