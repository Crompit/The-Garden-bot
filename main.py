
import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
from flask import Flask
from threading import Thread

# ======= WEB SERVER FOR 24/7 HOSTING =======
app = Flask('')

@app.route('/')
def home():
    return "✅ The Garden Bot is alive 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ======= DISCORD BOT SETUP =======
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ======= SIMPLE FEATURES =======

@bot.event
async def on_ready():
    print(f"🌱 The Garden is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def say(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🌿 The Garden Bot Commands", color=discord.Color.green())
    embed.add_field(name="🏓 !ping", value="Check bot latency.", inline=False)
    embed.add_field(name="🗣 !say <message>", value="Bot repeats your message.", inline=False)
    embed.add_field(name="💌 !confess <message>", value="Send anonymous confession.", inline=False)
    embed.add_field(name="💰 !daily", value="Claim daily coins.", inline=False)
    embed.add_field(name="💸 !balance", value="Check your balance.", inline=False)
    embed.add_field(name="⏰ !remind <time> <task>", value="Set a reminder. e.g., !remind 10m water plants", inline=False)
    embed.set_footer(text="🌱 The Garden • Made with love")
    await ctx.send(embed=embed)

# ======= ECONOMY SYSTEM =======
user_balances = {}

@bot.command()
async def daily(ctx):
    amount = random.randint(50, 150)
    user_balances[ctx.author.id] = user_balances.get(ctx.author.id, 0) + amount
    await ctx.send(f"💰 {ctx.author.mention}, you earned {amount} coins today!")

@bot.command()
async def balance(ctx):
    coins = user_balances.get(ctx.author.id, 0)
    await ctx.send(f"💸 {ctx.author.mention}, you have {coins} coins.")

# ======= REMINDER =======
@bot.command()
async def remind(ctx, time: str, *, task: str):
    unit = time[-1]
    if unit not in ["s", "m", "h"]:
        await ctx.send("❌ Invalid time format! Use s, m, or h.")
        return
    try:
        val = int(time[:-1])
    except:
        await ctx.send("❌ Invalid time value!")
        return
    seconds = val * {"s": 1, "m": 60, "h": 3600}[unit]
    await ctx.send(f"⏰ Reminder set! I’ll DM you in {time} to: {task}")
    await asyncio.sleep(seconds)
    await ctx.author.send(f"🔔 Reminder: {task}")

# ======= CONFESSION =======
@bot.command()
async def confess(ctx, *, message):
    confession_channel = discord.utils.get(ctx.guild.text_channels, name="confessions")
    if confession_channel:
        await confession_channel.send(f"💌 Anonymous Confession: {message}")
        await ctx.send("✅ Confession sent anonymously.")
    else:
        await ctx.send("❌ No #confessions channel found!")

# ======= KEEP ALIVE + START BOT =======
keep_alive()
bot.run(os.environ['TOKEN'])
