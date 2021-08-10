import discord
from discord.ext import commands
from bot.python_game_commands import bot_python

db = "bot/gamedb.db"

game_com = bot_python.GameCommands(db)

def GameCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_start(self):
		print("Bot is ready!")

	@commands.command(name='join'):
	async def join(self, ctx, player_class):
		if player_class not in ["Warrior"]:
			await ctx.send("Invalid Class")
		else:
			await ctx.send(game_com.new_player((str(ctx.author.id), str(player_class))))