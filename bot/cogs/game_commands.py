import discord
from discord.ext import commands
from bot.python_game_commands import bot_python
from bot.python_game_commands import hunt_system

db = "bot/gamedb.db"

game_com = bot_python.GameCommands(db)
hunt_sys = hunt_system.MonsterTable(db)

class Commands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bot is ready!")


	@commands.command(name='join')
	async def new_join(self, ctx, player_class=None):
		if player_class == None:
			await ctx.send(game_com.new_player((str(ctx.author.id), str(player_class))))
		else:
			await ctx.send(game_com.new_player((str(ctx.author.id), str(player_class))))


	@commands.command(name='shop')
	async def join(self, ctx):
		list_of_items = game_com.check_shop()
		embed = discord.Embed(title="Village Shop")
		for item in list_of_items:
			embed.add_field(name=f"**{item[0]}**", value=f"*item price*: {item[4]} pcs of silver\n*item type*:  {item[3]}\n*description*:\n{item[1]}", inline=False)
		await ctx.send(embed=embed)


	@commands.command(name='wealth')
	async def check_wealth(self, ctx):
		gold, silver, copper = game_com.get_wealth(ctx.author.id)[0]
		embed = discord.Embed(title=f"Wealth of {ctx.author.name}")
		embed.add_field(name=f"*Pieces of Gold* : {gold}", value=f"Now this is {ctx.author.name}'s True wealth.", inline=False)
		embed.add_field(name=f"*Pieces of Silver* : {silver}", value=f"This is {ctx.author.name}'s Riches.", inline=False)
		embed.add_field(name=f"*Pieces of Copperr* : {copper}", value=f"This is {ctx.author.name}'s Asset.", inline=False)
		await ctx.send(embed=embed)
	

	@commands.command(name="buy")
	async def player_buys(self, ctx, item_amount=1, *args):
		item_name = " ".join([word for word in args])
		content = game_com.buy(str(ctx.author.id), item_name, item_amount)
		embed = discord.Embed(title="Insuficient Funds")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"Cause of decline on buying {item_name}", value=f"{content}", inline=False)
		await ctx.send(embed=embed)
	

	@commands.command(name="sell")
	async def player_sells(self, ctx, item_amount=1, *args):
		item_name = " ".join([word for word in args])
		content = game_com.sell(str(ctx.author.id), item_name, item_amount)
		embed = discord.Embed(title="Insuficient source")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"Cause of decline on selling {item_name}", value=f"{content}", inline=False)
		await ctx.send(embed=embed)


	
	

	@commands.command(name="inv")
	async def player_inventory(self, ctx):
		inventory = game_com.get_user_inventory(str(ctx.author.name))
		if inventory == []:
			embed = discord.Embed(title=f"{ctx.author.name}'s Cosmic Inventory")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"{ctx.author.name}'s Cosmic Space", value=f"empty...") 
			await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Commands(bot))