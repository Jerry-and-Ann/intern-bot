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




# 1. Help Command
@bot.command(name='command')
async def help_command(ctx):
    help_text = """
**🛠️ Jerry&Ann Intern Bot Commands**

`!register` - Create your own private channel to submit work and ask questions.
`!command` - Get the welcome message and onboarding guide.
`!calendar` - Get access to the project calendar.
`!help` - Display this list of commands.
"""
    await ctx.send(help_text)

# 2. Hello Command
WELCOME_CHANNEL_NAME = "🎟welcome-hall"  # Replace with your actual channel name

@bot.command(name='hello')
async def hello(ctx):
    welcome_channel = discord.utils.get(ctx.guild.text_channels, name=WELCOME_CHANNEL_NAME)
    user = ctx.author

    if ctx.channel != welcome_channel:
        await ctx.send(f"{user.mention}, please use this command in {welcome_channel.mention}.")
        return

    # Delete all messages in the welcome channel
    async for message in welcome_channel.history(limit=100):
        try:
            await message.delete()
        except discord.Forbidden:
            pass

    # Personalized welcome message
    welcome_text = f"""
👋 **Hey {user.display_name}, welcome to the Jerry&Ann Social Media HQ!**

We're beyond excited to have you join our creative intern squad! Here’s your getting-started guide:

🔹 **Step 1: Read the Rules**  
Check out **#rules** to understand what’s cool and what’s not.

🔹 **Step 2: Assign Your Role**  
(Use Carl-bot reactions if available or wait for a manual role from an Admin.)

🔹 **Step 3: Explore the Channels**  
You’ll see platform-specific spaces like **#instagram-team**, **#reels-editing**, and more based on your work.

🔹 **Step 4: Check for Tasks**  
Pop into **#tasks-board** for your weekly goals, briefs, and updates.

🔹 **Step 5: Say Hello!**  
Hop into **#general-social-team** and introduce yourself – name, college, and your favorite social media platform!

💡 *Pro Tip:*  
Admins and Team Leads are always here if you’re unsure about anything. Don’t hesitate to reach out!

Let’s make **Jerry&Ann** shine online 💙  
**Welcome aboard, {user.display_name}!** 🚀
"""

    # Send message to channel
    msg = await welcome_channel.send(welcome_text)
    await msg.add_reaction("💙")  # Reaction for personal touch

    # Try DMing the user
    try:
        await user.send(welcome_text)
    except discord.Forbidden:
        await welcome_channel.send(f"{user.mention}, I couldn’t DM you the welcome guide. Please check your privacy settings.")



# 3. Calendar Command
@bot.command(name='calendar')
async def calendar(ctx):
    await ctx.send("📅 Here's the team calendar: https://your-calendar-link.com (Replace with actual link)")





keep_alive() # Ignore this command keep it unchanged
bot.run(TOKEN)
