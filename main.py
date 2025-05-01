import os
import sys
import traceback
import asyncio
from random import randint

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from dotenv import load_dotenv
from functools import wraps

# Load environment variables from .env file
load_dotenv()

# Parse developer IDs (comma-separated) into a set of ints
_DEVS = os.getenv("DEVELOPER_IDS", "").split(",")
DEVELOPER_IDS = {int(i) for i in _DEVS if i.strip().isdigit()}

# Bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure intents: allows reading messages and member list
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # Required to fetch guild members

# Initialize bot with prefix commands (!) and slash commands support
bot = commands.Bot(command_prefix="!", intents=intents)

separator = "-" * 20


def with_error_handling():
    """
    Decorator to wrap both slash (Interaction) and prefix (Context) commands
    with error catching. Logs full traceback to stderr, then sends a concise
    error message in Discord. Full details are only shown if a developer
    is present in the guild.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # First argument is either Context (prefix) or Interaction (slash)
            ctx = args[0]
            try:
                await func(*args, **kwargs)
            except Exception as err:
                # Log full traceback to stderr for debugging
                header = f"[ERROR]: Exception in `{func.__name__}`"
                trace = traceback.format_exc().rstrip()
                print(f"{header}\n{trace}\n{separator}", file=sys.stderr)

                try:
                    # Determine if any developer IDs are present in the guild
                    guild = getattr(ctx, "guild", None)
                    developers_present = []
                    if guild:
                        async for member in guild.fetch_members():
                            if member.id in DEVELOPER_IDS:
                                developers_present.append(member.id)

                    # Construct user-facing error message
                    user_msg = (
                        f"**[ERROR]:** *An internal error occurred:*\n```{err}```"
                        if developers_present
                        else "**[ERROR]:** *An internal error occurred.*"
                    )

                    # Send the error message appropriately
                    if isinstance(ctx, Interaction):
                        # Use initial response if not yet done, otherwise follow-up
                        if not ctx.response.is_done():
                            await ctx.response.send_message(user_msg)
                        else:
                            await ctx.followup.send(user_msg)
                    elif isinstance(ctx, commands.Context):
                        await ctx.send(user_msg)
                except Exception as second_err:
                    # Log secondary errors to stderr
                    print(
                        f"[ERROR]: Failed to send Discord message: {err}\n"
                        f"Secondary error: {second_err}\n{separator}\n",
                        file=sys.stderr
                    )
        return wrapper
    return decorator


@bot.event
async def on_ready():
    """
    Called when the bot has successfully connected to Discord.
    Syncs slash commands and notifies in console.
    """
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n{separator}")
    try:
        synced = await bot.tree.sync()
        count = len(synced)
        label = "commands" if count != 1 else "command"
        print(f"Synced {count} {label}.")
    except Exception as sync_err:
        print(f"[ERROR]: Command sync failed: {sync_err}")
    print(f"{bot.user.name} is online and ready to take over the galaxy!\n{separator}")


# --------------------
# Prefix Commands (!)
# --------------------

# Bootup command
@bot.command()
@with_error_handling()
async def bootup(ctx: commands.Context):
    """
    Simple bootup confirmation command for prefix usage.
    """
    await ctx.send("*Bootup complete.* **⚠️ UNIT OPERATIONAL. GREETINGS, HUMAN.**")


# --------------------
# Slash Commands (/)
# --------------------

# Greet command
@bot.tree.command(name="greet", description="Ominous Deathbot greeting.")
@with_error_handling()
async def greet(interaction: Interaction):
    """
    Slash command that sends an ominous greeting.
    """
    await interaction.response.send_message("**Deathbot** acknowledges your existence... for now")


# Self-destruct command
@bot.tree.command(name="selfdestruct", description="Deathbot self-destruct sequence.")
@with_error_handling()
async def selfdestruct(interaction: Interaction):
    """
    Initiates a dramatic countdown with flashing DND/online status.
    """
    # Send initial countdown message
    await interaction.response.send_message(
        "**[DEATHBOT PROTOCOL 9.11 ENGAGED]** INITIATING SELF-DESTRUCT SEQUENCE. T-MINUS: **5**..."
    )
    message = await interaction.original_response()

    # Countdown loop with half-second status flashes
    for i in range(8, -1, -1):
        # Alternate between DND (red) and online every half-second
        status = discord.Status.dnd if i % 2 == 0 else discord.Status.online
        await bot.change_presence(status=status)
        # Update countdown every full second
        if i % 2 == 0:
            await message.edit(
                content=(f"**[DEATHBOT PROTOCOL 9.11 ENGAGED]** INITIATING SELF-DESTRUCT SEQUENCE. T-MINUS: **{int(i/2)}**...")
            )
        await asyncio.sleep(0.5)
        await bot.change_presence(status=discord.Status.online)

    await asyncio.sleep(1)

    # Determine final outcome randomly
    if randint(1, 3) == 2:
        await bot.change_presence(status=discord.Status.dnd)
        await interaction.followup.send("**[WARNING]:** CRITICAL DAMAGE DETECTED. SHUTDOWN IMMINENT")
        await asyncio.sleep(2)
        await bot.change_presence(status=discord.Status.invisible)
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.online)
        await interaction.followup.send("**SYSTEM REBOOT COMPLETE.** DAMAGE PATCHED. DEATHBOT IS ONLINE.")
    else:
        await message.edit(
            content=(
                "**[DEATHBOT PROTOCOL 9.11 ENGAGED]** T-MINUS: **0**...\n"
                "**ERROR:** SAFETY LOCK ENGAGED. SELF DESTRUCTION ABORTED."
            )
        )


# America command
@bot.tree.command(name="america", description="WTF is a kilometer?")
@with_error_handling()
async def america(interaction: Interaction):
    """
    Sends a link to express Deathbot's truly American and patriotic confusion about what the kilometer is.
    """
    # Send a link
    await interaction.response.send_message("[What the FUCK is a kilometer?](https://whatthefuckisakilometer.com/embed-video)")


# Threaten command
@bot.tree.command(name="threaten", description="Threaten a user.")
@app_commands.describe(user="The user to threaten")
@with_error_handling()
async def threaten(interaction: Interaction, user: discord.User):
    """
    Sends a threat to the specified user in Discord chat.
    """
    # Send a link
    await interaction.response.send_message(f"{user.mention} — Your continued existence violates protocol `7-B`. You will be ***exfoliated*** with an orbital belt sander.")


# Start the bot
bot.run(TOKEN)
