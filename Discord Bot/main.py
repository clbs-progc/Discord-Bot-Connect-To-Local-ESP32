from urllib import response

import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import requests

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
admin_id = # Replace with the actual admin ID
bot = commands.Bot(command_prefix='!', intents=intents)

def connecttoesp(ipserver):
	try:
		response = requests.get(ipserver, timeout=(3,5) )
		if response.status_code == 200:
			print(f"Connection successful! Status code: {response.status_code}")
			response.close()
			return 1

		else:
			print(f"Server responded, but with an error: {response.status_code}")
			response.close()
			return -1

	except requests.exceptions.ConnectTimeout:
		print("The server took too long to accept the connection.")
		return 0

	except requests.exceptions.ReadTimeout:
		print("The server accepted the connection, but froze when sending headers.")
		return 0

	except requests.ConnectionError:
		print(f"Could not connect: {e}")
		return 0

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
	# Ignore messages sent by the bot itself
	if message.author == bot.user:
		return
	
	# Check if the channel is a DM
	#if isinstance(message.channel, discord.DMChannel):
	#    await message.channel.send("You are in my DMs!")

	#if "1234" in message.content.lower():
	#    await message.delete()
	#    await message.channel.send(f"{message.author.mention} - You mentioned banned word!")

	await bot.process_commands(message)

async def check_connection_error(ctx, connect, user): ##SENDS MESSAGE TO BOT'S OWNER ADMIN ID IN CASE OF ERROR
	if connect == -1:
		await user.send(f"Server responded but with an error HELP -1")
		await ctx.send(f"Server responded but with an error. <@{admin_id}> HELP")
	
	elif connect == 0:
		await user.send(f"Could not connect to the server HELP 0")
		await ctx.send(f"Could not connect to the server. <@{admin_id}> HELP") 


@bot.command()
async def missu(ctx):
	await ctx.send(f"miss u too {ctx.author.mention}!")

@bot.command()
async def attention(ctx):
	connect = connecttoesp("http://192.168.0.184/on") 
	user = await bot.fetch_user(admin_id)
	if connect == 1:
		await ctx.send("LIGHT IS ON")
		await user.send("LIGHT WAS TURNED ON") #SENDS MESSAGE TO ADMIN ID WHEN LIGHT IS TURNED ON 

	else:
		await check_connection_error(ctx, connect, user) #if not 1, its an error.
		

@bot.command()
async def off(ctx):
	connect = connecttoesp("http://192.168.0.184/off") #sends message in the chat where the !off was sent
	user = await bot.fetch_user(admin_id)
	if connect == 1:
		await ctx.send("LIGHT IS OFF")

	else:
		await check_connection_error(ctx, connect, user) #if not 1, its an error.

bot.run(token, log_handler=handler, log_level=logging.DEBUG)