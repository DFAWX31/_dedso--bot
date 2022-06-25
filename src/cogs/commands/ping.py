from discord.ext import bridge, commands


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="replies with the bot's latency")
    async def ping(self, ctx):
        await ctx.respond(f"Pong!🏓 {round(self.bot.latency* 1000, 2)}ms")


def setup(bot):
    bot.add_cog(PingCog(bot))
