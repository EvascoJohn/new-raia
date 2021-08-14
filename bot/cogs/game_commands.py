import discord
import threading
import time
from discord.ext import commands
from bot.python_game_commands import bot_python

db = "bot/gamedb.db"

game_com = bot_python.GameCommands(db)
game_hun = bot_python.Hunt(db)
cur = bot_python.CurrencyValues(db)

class Commands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bot is ready!")
		print("currency countdown started.")
		cur.run()
		def update():
			while 1:
				time.sleep(0.7)
				if int(time.strftime("%M")) == 15 and int(time.strftime("%S")) == 0:
					print("time to update")
					cur.run()
					pass
				else:
					pass
		t1 = threading.Thread(target=update)
		t1.start()

	@commands.command(name='join', description="use this command if you want to join the game.")
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

	@commands.command(aliases=['buy', 'b'])
	async def player_buys(self, ctx, item_amount=1, *args):
		item_name = " ".join([word for word in args])
		content = game_com.buy(str(ctx.author.id), item_name, item_amount)
		embed = discord.Embed(title="Insuficient Funds")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"Cause of decline on buying {item_name}", value=f"{content}", inline=False)
		await ctx.send(embed=embed)	

	@commands.command(aliases=['sell', 's'])
	async def player_sells(self, ctx, item_amount=1, *args):
		item_name = " ".join([word for word in args])
		content = game_com.sell(str(ctx.author.id), item_name, item_amount)
		embed = discord.Embed(title="Insuficient source")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"Cause of decline on selling {item_name}", value=f"{content}", inline=False)
		await ctx.send(embed=embed)

	@commands.command(aliases=['hunt', 'h'])
	async def player_hunts(self, ctx):
		output = game_hun.initiate_fight(str(ctx.author.id))
		monster_name, monster_damage, copper_drop, player_hp = output
		if player_hp > 0:
			embed = discord.Embed(title="Result of the Hunt!")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"Result:", value=f"""
					**{ctx.author.name}** encountered a **{monster_name}** and won!, {ctx.author.name} earned **{copper_drop}** pieces of copper and took **{monster_damage}** damage! {ctx.author.name} has remaining **{player_hp}/100** health!.
				""", inline=False)
			await ctx.send(embed=embed)
		if player_hp == 0:
			embed = discord.Embed(title="Result of the Hunt!")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"Result:", value=f"""
					**{ctx.author.name}** encountered a **{monster_name}** and died :rofl:\n{ctx.author.name} took **{monster_damage}** damage\n{ctx.author.name}'s hp is **{player_hp}/100** and earned **Nothing**.
				""", inline=False)
			await ctx.send(embed=embed)
			await ctx.send(f"@everyone **{ctx.author.name}** died :rofl:")

	@commands.command(aliases=['inventory', 'inv'])
	async def player_inventory(self, ctx):
		inventory = game_com.get_user_inventory(str(ctx.author.name))
		if inventory == []:
			embed = discord.Embed(title=f"{ctx.author.name}'s Cosmic Inventory")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"{ctx.author.name}'s Cosmic Space", value=f"empty...") 
			await ctx.send(embed=embed)

	@commands.command(aliases=['currex', 'cx'])
	async def player_seeks_values(self, ctx):
		c, s, g = cur.seeValues()
		embed = discord.Embed(title="Current Value of Currency")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"**copper** : {c}\n**silver** : {s}\n**gold** : {g}", value=f"\n**exchange desc:**\n1 silver = {c} of copper\n1 gold = {s} of silver\nthis happens vice versa!")
		await ctx.send(embed=embed)
	
	@commands.command(aliases=["copper to silver", "cpr2silv"])
	async def copper_to_silver(self, ctx, amount):
		await ctx.send("command under dev")
	
	@commands.command(name="help")
	async def help(self, ctx):
		embed = discord.Embed(title="Help")
		embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"r/`join`", value="Adds the game to the game and gives them 1000 copper as starting money. Benefits will not work if the user has already joined.")
		embed.add_field(name=f"r/`hunt`, r/`h`", value="Kills a random monster that exists in your current location for ex. `Village`\nHunt will give you `xp` and `copper`.")
		embed.add_field(name=f"r/`shop`, r/`s`", value="Shows the shop of your current location.")
		embed.add_field(name=f"r/`currex`, r/`cr`", value="It shows the `currex` or **Current Exchange** `currex` shows the currency's value for trading your copper to silver and silver to copper, silver to gold gold to silver and gold to copper depending on your favor during its its highs and lows.\n\nCheck out **r/**`trade` for more details in exchange")
		embed.add_field(name=f"r/`trade, r/`t` `[amount] [currency to currency]`", value="for trading your copper to silver and silver to copper, silver to gold gold to silver and gold to copper depending on your favor during its highs and lows. Being able to utilize this method can be an alternative to `hunt` for gaining copper, and in the long run to join the **leaderboards** where your `gold` will be taken into account.\n\nSince this game has 3 currencies `copper`, `silver` and `gold`. In this game you will only accumalate copper during you `hunt`'s, and you will only spend `silver` on the shop, while `gold` the top of Currency Exchange will make you wealthier, managing how you trade will be an alternative for getting copper during you hunts.")
		await ctx.send(embed=embed)
	
	@commands.command(name="travel")
	async def player_trancends(self, ctx):
		await ctx.send("travelling is under development By the Cafe, just chillax and sip some of that :coffee:")

	@commands.command(aliases=['trade', 't'])
	async def player_trade(self, ctx, amount=0, *args):
		command = " ".join([word for word in args])
		output = cur.copper_to_silver(str(ctx.author.id), amount)
		if command == "copper to silver" and output != "not enough silver.":
			copper, silver = output
			embed = discord.Embed(title="Trade of silver to copper!")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"A trade of {int(copper)*amount} pieces Copper for an amount of {amount} Silver ", value=f"**{ctx.author.name}** has traded {int(copper)*amount} pieces of copper for an amount of {amount} Silver", inline=False)
			await ctx.send(embed=embed)
		
		else:
			embed = discord.Embed(title="Trade Problem: Not enough resources.")
			embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Commands(bot))