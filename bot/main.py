from python_game_commands import bot_python
import flask_webserver as bot_webserver
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

#load the token
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


bot = commands.Bot(command_prefix='r/')


bot.load_extension("cogs.game_commands")


def run():
	bot_webserver.keep_alive()
	bot.run(BOT_TOKEN)