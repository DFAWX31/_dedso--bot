from discord.ext import commands

class ReadyEvent(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"logged in as { self.bot.user }")

def setup(bot):
	bot.add_cog(ReadyEvent(bot))