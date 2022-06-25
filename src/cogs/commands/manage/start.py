import discord
from discord.ext import commands, bridge
import sqlalchemy

from database.create import connection, ctf_table

class StartCTF(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description="start a ctf")
	async def start(self, ctx, ctf_name: discord.Option(str), date:discord.Option(str)):

		if ctf_table == None:
			return ctx.respond("table not found in database")

		s = sqlalchemy.select(ctf_table).where(ctf_table.c.name == ctf_name)

		ctf_exists = connection.execute(s).fetchall()

		for ctf in ctf_exists:
			if ctf[3]:
				return await ctx.respond(f"{ctf_name} already exists and is active")

		insert = ctf_table.insert().values(
			name=ctf_name, date=date, active=True
		)
		connection.execute(insert)

		return await ctx.respond(f"{ctf_name} succesfully added to database and all joins to this ctf by users will be accepted")


def setup(bot):
	bot.add_cog(StartCTF(bot))