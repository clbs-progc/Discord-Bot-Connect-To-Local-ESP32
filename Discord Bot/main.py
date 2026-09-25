from urllib import response

import random
import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import requests

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

SOURCE_PICS_CHANNEL_ID = #channel id
SOURCE_GIFS_CHANNEL_ID = #channel id
DEST_PICS_CHANNEL_ID = #channel id
DEST_GIFS_CHANNEL_ID = #channel id
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
admin_id = # Replace with the actual admin ID
bot = commands.Bot(command_prefix='!', intents=intents)

gif_list = [
    "https://tenor.com/",
    "https://tenor.com/",
    "https://tenor.com/"
]

def connecttoesp(ipserver):
	try:
		response = requests.get(ipserver, timeout=(3,5) )
		if response.status_code == 200:
			print(f"Connection successful! Status code: {response.status_code}")
			#print(response.text)
			random.seed(response.text)
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

	if message.channel.id == SOURCE_PICS_CHANNEL_ID:
		destination_channel = bot.get_channel(DEST_PICS_CHANNEL_ID)
		if destination_channel:
			try:
                # Prepare attachments if any exist in the original message
				files = []
				for attachment in message.attachments:
					files.append(await attachment.to_file())

                	# Construct a clean text format showing who sent the original message
                	#content_to_send = f"**{message.author.name}**: {message.content}" if message.content else f"**{message.author.name}** sent a file/embed:"
					

                # Send content and files to the destination channel in the other server
				await destination_channel.send(files=files)
				
			except Exception as e:
				print(f"Failed to copy message: {e}")
		
	if message.channel.id == SOURCE_GIFS_CHANNEL_ID:
		destination_channel = bot.get_channel(DEST_GIFS_CHANNEL_ID)
		content_to_send = ""
		if "http://" not in message.content and "https://" not in message.content:
			return

		if destination_channel:
			try:
                # Prepare attachments if any exist in the original message
				files = []
				for attachment in message.attachments:
					files.append(await attachment.to_file())

                	# Construct a clean text format showing who sent the original message
				if message.content:
					content_to_send = f"{message.content}"
					

                # Send content and files to the destination channel in the other server
				await destination_channel.send(content=content_to_send, files=files)
				
			except Exception as e:
				print(f"Failed to copy message: {e}")

	await bot.process_commands(message)

async def check_connection_error(ctx, connect, user): ##SENDS MESSAGE TO BOT'S OWNER ADMIN ID IN CASE OF ERROR
	if connect == -1:
		await user.send(f"Server responded but with an error HELP -1")
		await ctx.send(f"Server responded but with an error. <@{admin_id}> HELP")
	
	elif connect == 0:
		await user.send(f"Could not connect to the server HELP 0")
		await ctx.send(f"Could not connect to the server. <@{admin_id}> HELP") 


@bot.command()
async def ping(ctx):
	await ctx.send(f"PONG! {round(bot.latency * 1000)}ms")

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

@bot.command()
async def gif(ctx):
    # Get the specific channel where images are stored
    source_channel = bot.get_channel(DEST_GIFS_CHANNEL_ID)
    
    if not source_channel:
        await ctx.send("Could not find the source image channel. Check the ID!")
        return

    gif_messages = []

    # Fetch history from the SPECIFIC source channel
    async for message in source_channel.history(limit=200):
        if any(keyword in message.content for keyword in ["tenor.com", "giphy.com", ".gif"]):
            gif_messages.append(message.content)
            continue

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type == "image/gif":
                    gif_messages.append(attachment.url)

    if not gif_messages:
        await ctx.send(f"No gifs found in the source channel!")
        return
	
    gif_messages.extend(gif_list)
    chosen_gif_url = random.choice(gif_messages)

    await ctx.send(f"{chosen_gif_url}")

@bot.command()
async def pic(ctx):
    # Get the specific channel where images are stored
    source_channel = bot.get_channel(DEST_PICS_CHANNEL_ID)
    
    if not source_channel:
        await ctx.send("Could not find the source image channel. Check the ID!")
        return

    image_messages = []

    # Fetch history from the SPECIFIC source channel
    async for message in source_channel.history(limit=200):
        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                    image_messages.append(attachment.url)

    if not image_messages:
        await ctx.send(f"No images found in the source channel!")
        return

    chosen_image_url = random.choice(image_messages)

    await ctx.send(f"Here is a random pic :)\n{chosen_image_url}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)