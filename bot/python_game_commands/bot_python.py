import sqlite3
import random
import threading


class ShortDBCommands(object):

	def create_connection(self):
		self._connection = sqlite3.connect(self.database)
		self._connection.execute("""PRAGMA foreign_keys=ON;""")

	def create_cursor(self):
		self.create_connection()
		self._cursor = self._connection.cursor()

	def exec_with_commit(self, sqlite_line):
		self.create_cursor()
		self._cursor.execute(sqlite_line)
		self._connection.commit()
		self._cursor.close()
		self._connection.close()

	def exec_with_fetchall(self, sqlite_line):
		self.create_cursor()
		output = self._cursor.execute(sqlite_line).fetchall()
		self._connection.commit()
		self._cursor.close()
		self._connection.close()
		return output

	def exec_with_fetchone(self, sqlite_line):
		self.create_cursor()
		output = self._cursor.execute(sqlite_line).fetchone()
		self._connection.commit()
		self._cursor.close()
		self._connection.close()
		return output



class GeneralPlayers(ShortDBCommands):

	def __init__(self, database):
		""" Initiallizes __init__ with database """
		self.database = database

	def add_player(self, player_id):
		""" runs the "sql_line" then accompanies it with commit. """
		try:
			self.exec_with_commit(f"""	INSERT INTO GeneralPlayersDatabase(discord_id)
										VALUES("{player_id}");
									""")
		except sqlite3.IntegrityError as e:
			#this will trigger if the player_id is already in the database
			if e.args[0] == "UNIQUE constraint failed: GeneralPlayersDatabase.discord_id":
				return "Player Already Exists"

			#this will trigger if the player_class is not in the database.
			elif e.args[0] == "FOREIGN KEY constraint failed":
				return "Player Class Invalid"
		else:
			#this will trigger if the player is not yet in the database when added.
			return "Welcome new player"


	def get_player(self, player_id):
		output = self.exec_with_fetchone(f"""
										SELECT "discord_id","player_hp" FROM GeneralPlayersDatabase WHERE discord_id="{player_id}"
								""")
		return output

	def set_player_health(self, player_id, hp):
		self.exec_with_commit(f"""
			UPDATE GeneralPlayersDatabase SET "player_hp" = {hp} WHERE "discord_id"="{player_id}"
			""")


	def get_class(self, player_id):
		pass



class WorldInventory(ShortDBCommands):

	def __init__(self, database):
		self.database = database

	def get_user_inventory(self, player_id):
		list_of_items = []
		items = self.exec_with_fetchall(f"""
				SELECT * FROM WorldInventory WHERE "owner_id"="{player_id}"
			""")
		return items

	#adds an item to the players inventory.
	def add_user_item(self, player_id, item_name):
		#updates table
		checks_item = self.exec_with_fetchall(f"""
				SELECT * FROM WorldInventory WHERE "item_name"="{item_name}" AND "owner_id"="{player_id}"
			""")
		if checks_item:
			return checks_item
		else:
			return None



class TableOfWealth(ShortDBCommands):

	def __init__(self, database):
		self.database = database
  
	def add_gold(self, player_id, amount):
		#increases gold
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "gold" = "gold" + {amount} WHERE "owner_id"="{player_id}"
			""")

	def starter(self, player_id):
		acc_exists = self.exec_with_fetchall(f""" SELECT * FROM TableOfWealth WHERE "owner_id"="{player_id}" """)
		if acc_exists == []:
			self.exec_with_commit(f"""
					INSERT INTO TableOfWealth(owner_id, gold, silver, copper) VALUES("{player_id}", 0, 0, 1000)
				""")

	def add_silver(self, player_id, amount):
		#increases silver
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "silver" = "silver" + {amount} WHERE "owner_id"="{player_id}"
			""")

	def add_copper(self, player_id, amount):
		#increases copper
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "copper" = "copper" + {amount} WHERE "owner_id"="{player_id}"
			""")

	def deduct_gold(self, player_id, amount):
		#decreases gold
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "gold" = "gold" - {amount} WHERE "owner_id"="{player_id}"
			""")

	def deduct_silver(self, player_id, amount):
		#decreases silver
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "silver" = "silver" - {amount} WHERE "owner_id"="{player_id}"
			""")

	def deduct_copper(self, player_id, amount):
		#decrases silver
		self.exec_with_commit(f"""
				UPDATE TableOfWealth SET "copper" = "copper" - {amount} WHERE "owner_id"="{player_id}"
			""")

	def get_wealth(self, player_id):
		output = self.exec_with_fetchall(f""" SELECT "gold", "silver", "copper" FROM TableOfWealth WHERE "owner_id"="{player_id}" """)
		print(output)
		return output



class ConsumableItemsDatabase(ShortDBCommands):

	def __init__(self, database):
		self.database = database

	def get_item_name(self, item_name):
		items = [item_tuple for item in self.exec_with_fetchall(f"""
					SELECT "item_name", "item_description", "health_regen", "item_type", "item_price" FROM VillageConsumablesItems
					WHERE "item_name"="{item_name}" """)]
		return items



class WeaponItemsDatabase(ShortDBCommands):

	def __init__(self, database):
		self.database = database

	def get_item_name(self, item_name):
		output = self.exec_with_fetchall(f"""
					SELECT "item_name", "item_description", "Damage", "item_type", "item_price" FROM VillageWeaponItems
					WHERE "item_name"="{item_name}" """)
		return output



class CurrencyValues(object):

		def run(self):
			import currency_dictator as cd
			cd.run()
			self.copper = cd.copper
			self.silver = cd.silver
			self.gold = cd.gold

		def trade(self):
			print(self.copper)
			print(self.silver)
			print(self.gold)


class VillageShop(WorldInventory, TableOfWealth):

	def __init__(self, database):
		self.database = database

	def shop(self):
		output = self.exec_with_fetchall(f"""
			SELECT * FROM VillageShop
			""")
		return output

	def buy(self, player_id, item_name, amount=1):
		#gets the item price
		item_cost = self.exec_with_fetchone(f"""
				SELECT "item_price" FROM VillageShop WHERE "item_name"="{item_name}"
			""")
		item_exists = self.exec_with_fetchone(f"""
				SELECT "item_name" FROM VillageShop WHERE "item_name"="{item_name}"
			""")
		if not item_exists:
			return "item not found"
		#gets player inventory
		total_amount = int(item_cost[0]) * amount
		check_item_exists = self.add_user_item(player_id,item_name)
		#if the player has an existing item, add an amount.
		if check_item_exists == None:
			try:
				self.deduct_silver(player_id, total_amount)
				self.exec_with_commit(f"""
						INSERT INTO WorldInventory(owner_id, item_name, item_amount)
						VALUES("{player_id}", "{item_name}", {amount})
					""")
			except sqlite3.IntegrityError as e:
				if e.args[0] == "FOREIGN KEY constraint failed":
					return "..."
				
				return e.args[0]
		elif check_item_exists[0] != None:
			try:
				self.deduct_silver(player_id, total_amount)
				self.exec_with_commit(f"""
						UPDATE WorldInventory SET "item_amount"="item_amount" + {amount} WHERE "owner_id"="{player_id}" AND "item_name"="{item_name}"
					""")
			except sqlite3.IntegrityError as e:
				if e.args[0] == "FOREIGN KEY constraint failed":
					return "Player does not yet exist in the game"
				
				return e.args[0]
		return "item succesfully baught."

	def sell(self, player_id, item_name, amount):
		#gets the item price
		item_cost = self.exec_with_fetchone(f"""
				SELECT "item_price" FROM VillageShop WHERE "item_name"="{item_name}"
			""")
		item_exists = self.exec_with_fetchone(f"""
				SELECT "item_name", "owner_id" FROM WorldInventory WHERE "item_name"="{item_name}" AND "owner_id"="{player_id}"
			""")
		if not item_exists:
			return "Player has no such item."
		#gets player inventory
		total_amount = int(item_cost[0]) * amount
		check_item_exists = self.add_user_item(player_id,item_name)
		#if the player has an existing item, add an amount.
		if check_item_exists == None:
			try:
				self.add_silver(player_id, total_amount)
				self.exec_with_commit(f"""
						INSERT INTO WorldInventory(owner_id, item_name, item_amount)
						VALUES("{player_id}", "{item_name}", {amount})
					""")
			except sqlite3.IntegrityError as e:
				if e.args[0] == "FOREIGN KEY constraint failed":
					return "Player does not yet exist in the game."
				
				return e.args[0]
		elif check_item_exists[0] != None:
			try:
				self.add_silver(player_id, total_amount)
				self.exec_with_commit(f"""
						UPDATE WorldInventory SET "item_amount"="item_amount" - {amount} WHERE "owner_id"="{player_id}" AND "item_name"="{item_name}"
					""")
			except sqlite3.IntegrityError as e:
				if e.args[0] == "FOREIGN KEY constraint failed":
					return "Player does not yet exists in the game"
				
				return e.args[0]
		return "item succesfully sold."



class MonsterTable(ShortDBCommands):

	def __init__(self, database):
		self.database = database

	def get_monster(self):
		import random
		monsters = self.exec_with_fetchall("""
					SELECT * FROM MonsterTable
			""")
		pick = monsters[int(random.randint(0, len(monsters)-1))]
		name, damage, health, copper_drop = pick
		return pick

 

class Hunt(GeneralPlayers, MonsterTable, TableOfWealth):

	def __init__(self, database):
		self.database = database

	def initiate_fight(self, player_id):
		#get random monster stats
		monster_list = self.get_monster()
		name, damage, health, copper_drop = monster_list
		#get player stats
		player_id, player_hp = self.get_player(player_id)
		damage = 20
		if damage >= player_hp:
			self.set_player_health(player_id, 100)
			return "Player Died."
		elif damage < player_hp:
			player_hp = player_hp - damage
			self.set_player_health(player_id, player_hp)
			self.add_copper(player_id, copper_drop)
		return name, damage, copper_drop, player_hp


class GameCommands(GeneralPlayers, VillageShop, TableOfWealth):

	def __init__(self, database):
		super().__init__(database)#Initallizes the GeneralPlayers class.

	def new_player(self, player_id):
		#the line for inserting.
		output = self.add_player(player_id)
		self.starter(player_id)
		return output

	def seek_player(self, player_id):
		return self.get_player(player_id)

	def check_shop(self):
		return self.shop()



if __name__ == "__main__":
	import time
	db ="GameDB.db"
	i = "519807756711649291"
	c = "Warrior"
	gc = GameCommands(db)
	h = Hunt(db)
	cur = CurrencyValues()


	def update():
		while 1:
			time.sleep(0.7)
			if int(time.strftime("%M")) == 26 and int(time.strftime("%S")) == 0:
				print("time to update")
				cur.run()
				cur.trade()

	t1 = threading.Thread(target=update)
	t1.start()