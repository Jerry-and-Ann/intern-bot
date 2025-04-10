from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()








import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


TOKEN = os.getenv("BOT_TOKEN")
load_dotenv()  # loads .env file into environment variables

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Required to read messages

bot = commands.Bot(command_prefix='!', intents=intents)

# Set your admin role name and category name for private channels
ADMIN_ROLE_NAME = "Admin"
PRIVATE_CATEGORY_NAME = "Intern Channels"

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command()
async def register(ctx):
    guild = ctx.guild
    user = ctx.author
    existing_channel_name = f"intern-{user.name.lower()}"

    # Check if a channel already exists for this user
    for channel in guild.text_channels:
        if channel.name == existing_channel_name:
            await ctx.send(f"{user.mention} You already have a private channel: {channel.mention}")
            return

    # Find or create category
    category = discord.utils.get(guild.categories, name=PRIVATE_CATEGORY_NAME)
    if not category:
        category = await guild.create_category(PRIVATE_CATEGORY_NAME)

    # Set permissions
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

    # Allow admin role to see all
    admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE_NAME)
    if admin_role:
        overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    # Create the channel
    channel = await guild.create_text_channel(
        name=existing_channel_name,
        overwrites=overwrites,
        category=category,
        topic=f"Private channel for {user.display_name}"
    )

    await channel.send(f"👋 Welcome {user.mention}!\nThis is your private workspace. You can submit drafts, ask questions, or track your work here.")
    await ctx.send(f"{user.mention} Your private channel has been created: {channel.mention}")

keep_alive()
bot.run(TOKEN)
