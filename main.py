import asyncio
from random import randint

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load secret environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Create the bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# On ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command{"s"if len(synced) > 1 else ''}")
    except Exception as e:
        print(f"Sync failed: {e}")
    print(f"{bot.user.name} is online and ready to take over the galaxy!")

# ! commands

# Bootup command
@bot.command()
async def bootup(ctx):
    await ctx.send("*Bootup Complete.* **⚠️ THIS UNIT IS FULLY FUNCTIONAL. GREETINGS, HUMAN.**")


# Slash commands

# Greet command
@bot.tree.command(name="greet", description="Ominous Deathbot greeting.")
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message("**Deathbot** acknowledges your existence... for now")

@bot.tree.command(name="selfdestruct", description="Deathbot selfdestruct sequence")
async def selfdestruct(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(
            "**[DEATHBOT PROTOCOL 9.11 ENGAGED]** INITIATING SELF-DESTRUCT SEQUENCE. T-MINUS: **5**...",
            ephemeral=False
        )
        message = await interaction.original_response()

        for i in range(8, -1, -1):
            status = discord.Status.dnd if i % 2 == 0 else discord.Status.online
            await bot.change_presence(status=status)
            if i % 2 == 0:
                await message.edit(content=f"**[DEATHBOT PROTOCOL 9.11 ENGAGED]** INITIATING SELF-DESTRUCT SEQUENCE. T-MINUS: **{int(i / 2)}**...")
            await asyncio.sleep(0.5)
            await bot.change_presence(status=discord.Status.online)


        await asyncio.sleep(1)
        if randint(1, 2) == 2:
            await bot.change_presence(status=discord.Status.dnd)
            await interaction.followup.send("**[WARNING]:** CRITICAL DAMAGE DETECTED. SHUTDOWN IMMINENT")
            await asyncio.sleep(2)
            await bot.change_presence(status=discord.Status.invisible)
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.online)
            await interaction.followup.send("**SYSTEM REBOOT COMPLETE.** DAMAGE PATCHED. DEATHBOT IS ONLINE.")
        else:
            await message.edit(content=(
                    "**[DEATHBOT PROTOCOL 9.11 ENGAGED]** T-MINUS: **0**...\n" +
                    "**ERROR:** SAFETY LOCK ENGAGED. SELF DESTRUCTION ABORTED."
            ))
    except Exception as e:
        await interaction.response.send_message(f"**[ERROR]:** *An internal error has occurred:*\n{e}")


# Run the bot with the bot token
bot.run(TOKEN)
