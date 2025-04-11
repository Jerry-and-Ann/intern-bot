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
`!hello` - Get the welcome message and onboarding guide.
`!resources` - Get access to the project calendar.
`!command` - Display this list of commands.
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

    We're absolutely thrilled to have you as part of our vibrant intern squad! This is your launchpad to a creative and collaborative journey. 🚀

    Here’s everything you need to get started:

    🔹 **Step 1: Read the Rules**  
    Head over to **#rules** to understand what’s encouraged and what to avoid — we keep it chill, respectful, and fun.

    🔹 **Step 2: Claim Your Private Channel**  
    Jump into **#intern-assigning** and type `!register`. This creates your **own private workspace** where you can talk to your Manager, Team Lead, or even the Founders directly.

    🔹 **Step 3: Say Hello to the Team**  
    🎉 Time to make your grand entrance!
    Hop into #general-social-team and tell us all the juicy stuff. We wanna know:

    🙋‍♀️ Your name
    😂 One funny/quirky thing about you (Do you talk to plants? Collect weird mugs? We’re all ears!)
    🌟 One thing you’re really proud of (Could be a skill, a trait, or just being a great plant parent 🌱)
    🎯 What you're here to learn during your time with us

    No pressure, just good vibes. Can’t wait to get to know the awesome human behind the name! ✨

    🔹 **Step 4: Explore the Channels**  
    You’ll find dedicated spaces like **#instagram-team**, **#linkedin-team**, and more — each one tailored to different projects and content styles.

    🔹 **Step 5: Check Your Task Channel**  
    Head to **#tasks-board** — that’s where team's briefs, assignments, and weekly goals will appear.

    💡 **Pro Tip:**  
    Stuck? Unsure? Curious? The **Admins** and **Leads** are just a ping away. Never hesitate to ask for help or share ideas!

    ---

    Let’s create something awesome together and make **Jerry&Ann** shine online 💙  
    **Welcome aboard, {user.display_name}! You’ve got this! 🌟**
    """


    # Send message to channel
    msg = await welcome_channel.send(welcome_text)
    await msg.add_reaction("💙")  # Reaction for personal touch

    # Try DMing the user
    try:
        await user.send(welcome_text)
    except discord.Forbidden:
        await welcome_channel.send(f"{user.mention}, I couldn’t DM you the welcome guide. Please check your privacy settings.")


# Resources
@bot.command(name='resources')
async def resources(ctx):
    embed = discord.Embed(
        title="📚 Intern Resources Hub",
        description="Here are your important working links to stay organized and efficient:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📅 Calendar",
        value="[Click Me](https://cheddar-random-832.notion.site/1d2516692e2180ac8302d47718730784?v=1d2516692e218088a1e1000ccff9189e)\nTrack all key dates, deadlines, and upcoming events.",
        inline=False
    )

    embed.add_field(
        name="🧰 Assets Library",
        value="[Click Me](https://cheddar-random-832.notion.site/1d2516692e218079bd15f6115b5ffa01?v=1d2516692e21806785a0000cf3ce28cd)\nAccess logos, templates, design files, and more.",
        inline=False
    )

    embed.add_field(
        name="📝 Meeting Notes",
        value="[Click Me](https://cheddar-random-832.notion.site/1d2516692e21805d8d44f4a9bb243ca1?v=1d2516692e2180f99c71000c1d12491a)\nCatch up on discussion points, action items, and decisions.",
        inline=False
    )

    embed.set_footer(text="Keep these links handy! Let’s stay aligned and creative 💡")

    # Send the embed and delete it after 60 seconds
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()






keep_alive() # Ignore this command keep it unchanged
bot.run(TOKEN)
