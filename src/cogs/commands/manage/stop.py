import discord
from discord.ext import bridge, commands

from database.create import connection, ctf_table


class StopCTF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="stop a running ctf")
    async def stop(self, ctx, ctf_name: discord.Option(str)):
        if ctf_table is None:
            return await ctx.respond(f"{ctf_name} not found in database")

        stmnt = ctf_table.update().where(ctf_table.c.name == ctf_name).values(active=False)

        connection.execute(stmnt)

        return await ctx.respond(f"succesfully marked {ctf_name} as finished")


def setup(bot):
    bot.add_cog(StopCTF(bot))
