from select import select
import discord
from discord.ext import commands, bridge
import sqlalchemy
from database.create import connection, ctf_teams, ctf_table

class SelectMenu(discord.ui.Select):
	def __init__(self, data:list, options:list, table:sqlalchemy.Table, points: int, disabled=False):
		self.data = data
		self.table = table
		self.points = points
		super().__init__(
			placeholder="Choose a ctf to join",
			options = options,
			disabled=disabled
		)
	
	async def callback(self, interaction):
		ctf_name = None
		for i in self.data:
			if self.values[0] == str(i[0]):
				ins = sqlalchemy.update(self.table).where(self.table.c.id == i[0]).values(points = self.points)

				print(ins)

				ctf_team = i[1]
				
				ctf_name = i[6]

				connection.execute(ins)

		await interaction.response.send_message(f"succesfully registered that {ctf_team} got {self.points} in {ctf_name} ctf")
		await interaction.message.edit(view = discord.ui.View(SelectMenu(self.data, self.options, self.table, self.points, True)))

class PointsCTF(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@bridge.bridge_command(description="Finalize how many points your team got int the cuttent ctf")
	async def final(self, ctx, points: discord.Option(int, "number of points you got")):
		
		getTeam = connection.execute(
			sqlalchemy.select(ctf_teams).where(ctf_teams.c.leader == str(ctx.author.id))
		).fetchall()

		if not getTeam:
			return await ctx.respond("Team with you as the leader could not be found!!")
		
		getActiveCTFs = connection.execute(
			sqlalchemy.select(ctf_table).where(ctf_table.c.active == True)
		).fetchall()

		true_cases = []

		for team in list(getTeam):
			for ctfs in list(getActiveCTFs):
				if list(team)[5] == list(ctfs)[0]:
					team = list(team)
					ctfs = list(ctfs)
					team.append(ctfs[1])
					true_cases.append(team)

		if not true_cases:
			return await ctx.respond("No active CTFs with you as the leader found in the database")

		if len(true_cases) > 1:
			options = []
			for case in true_cases:
				print(case)
				options.append(
					discord.SelectOption(
						label=case[1], value=str(case[0]), description=case[6]
					)
				)
			select = SelectMenu(true_cases, options, ctf_teams, points)

			view = discord.ui.View()
			view.add_item(select)

			return await ctx.respond("Please select the team of which you want to register the points for", view=view)
		
		await ctx.respond(f"Succesfully entered that team { true_cases[0][1] } got {points} in the {true_cases[0][6]} ctf")


def setup(bot):
	bot.add_cog(PointsCTF(bot))