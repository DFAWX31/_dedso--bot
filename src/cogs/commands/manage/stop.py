import discord
from discord.ext import commands, bridge
import sqlalchemy

from database.create import metadata_obj, connection, engine

class StopCTF(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description="stop a running ctf")
	async def stop(self, ctx, ctf_name: discord.Option(str)):

		ctf_table = sqlalchemy.Table(
			"ctf_table", metadata_obj, autoload_with=engine
		)

		if ctf_table == None:
			return await ctx.respond(f"{ctf_name} not found in database")

		stmnt = ctf_table.update().where(ctf_table.c.name == ctf_name).values(active=False)

		connection.execute(stmnt)

		return await ctx.respond(f"succesfully marked {ctf_name} as finished")


def setup(bot):
	bot.add_cog(StopCTF(bot))
