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
    print(f"{bot.user.name} is online and ready to take over the galaxy!")

# Placeholder greet command
@bot.command()
async def bootup(ctx):
    await ctx.send("*Bootup Complete.* **⚠️ THIS UNIT IS FULLY FUNCTIONAL. GREETINGS, HUMAN.**")


# slash command
@bot.tree.command(name="greet", description="Ominous Deathbot greeting.")
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message("**Deathbot** acknowledges your existence... for now.")

# Run the bot with the bot token
bot.run(TOKEN)
