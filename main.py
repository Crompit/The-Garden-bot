
import discord
from discord.ext import commands

TOKEN = ""  # Paste your bot token here

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Help command
@bot.command()
async def help(ctx):
    await ctx.send("📖 Commands: !ping, !meme, !confess, !balance, !remindme")

# Ping command
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Add other features here (invite tracker, economy, etc.)

bot.run(TOKEN)
