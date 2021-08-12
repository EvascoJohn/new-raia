import discord
from discord.ext import commands
from bot.python_game_commands import bot_python

db = "bot/gamedb.db"

game_com = bot_python.GameCommands(db)
game_hun = bot_python.Hunt(db)
cur = CurrencyValues()

class Commands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("currency countdown started.")
		def update():
			while 1:
				time.sleep(0.7)
				if int(time.strftime("%M")) == 26 and int(time.strftime("%S")) == 0:
					print("time to update")
					cur.run()
					cur.trade()
		t1 = threading.Thread(target=update)
		t1.start()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bot is ready!")

	@commands.command(name='join')
	async def new_join(self, ctx):
		await ctx.send(game_com.new_player((str(ctx.author.id))))

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

	@commands.command(name="hunt")
	async def player_hunts(self, ctx):
		output = game_hun.initiate_fight(str(ctx.author.id))

		if output != "Player Died.":
			monster_name, monster_damage, copper_drop, player_hp = output
			embed = discord.Embed(title="Result of the Hunt!")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"Result:", value=f"""
					**{ctx.author.name}** encountered a **{monster_name}**, earned **{copper_drop}** pieces of copper and took **{monster_damage}** damage! {ctx.author.name} has remaining **{player_hp}/100** health!.
				""", inline=False)
			await ctx.send(embed=embed)
		else:
			await ctx.send(output)

	@commands.command(name="inv")
	async def player_inventory(self, ctx):
		inventory = game_com.get_user_inventory(str(ctx.author.name))
		if inventory == []:
			embed = discord.Embed(title=f"{ctx.author.name}'s Cosmic Inventory")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"{ctx.author.name}'s Cosmic Space", value=f"empty...") 
			await ctx.send(embed=embed)

	@commands.command(name="currex")
	async def player_trades(self, ctx):
		await ctx.send("currex(Currency Exchange) is under development By the Cafe, just chillax and sip some of that :coffee:")

	
	@commands.command(name="travel")
	async def player_trancends(self, ctx):
		await ctx.send("travelling is under development By the Cafe, just chillax and sip some of that :coffee:")


def setup(bot):
	bot.add_cog(Commands(bot))