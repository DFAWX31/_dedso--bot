import discord
import sqlalchemy
from discord.ext import bridge, commands

from database.create import connection, ctf_table


class ViewCTF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(
        description="view all ctfs that have been registered in the database and are currently active"
    )
    async def view(self, ctx):
        if ctf_table is None:
            return await ctx.respond("Table not found")

        select = connection.execute(sqlalchemy.select(ctf_table).where(ctf_table.c.active is True)).fetchall()

        if len(list(select)) < 1:
            return await ctx.respond("No active ctfs found")

        if len(list(select)) > 0:
            embed = discord.Embed(title="Active CTFs right now", color=discord.Color.random())
            for li in list(select):
                li = list(li)

                embed.add_field(name=li[1], value=li[2], inline=False)
            return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ViewCTF(bot))
