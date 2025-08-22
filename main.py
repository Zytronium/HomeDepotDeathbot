import os
import sys
import traceback
import asyncio
from random import randint, choice, sample
from functools import wraps
from dotenv import load_dotenv

import discord
from discord import Interaction, app_commands
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

# Parse developer IDs (comma-separated) into a set of ints
_DEVS = os.getenv("DEVELOPER_IDS", "").split(",")
DEVELOPER_IDS = {int(i) for i in _DEVS if i.strip().isdigit()}

# Constant IDs
CREATOR_ID = int(os.getenv("CREATOR_ID", "405547931102609429"))
PHYL_ID = int(os.getenv("PHYL_ID", "1047614240778895462"))

# Bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure intents: allows reading messages and member list
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # Required to fetch guild members

# Initialize bot with prefix commands (!) and slash commands support
bot = commands.Bot(command_prefix="!", intents=intents)

separator = "-" * 20


def get_loadout():
    """
    Generate a random loadout for head, arms, and core.
    There are 3,537,952 unique possible combinations.
    """
    # Loadout lists
    head_loadouts = [
        "Standard Robotic",
        "Standard Robotic",  # Intentionally duplicated to decrease rarity
        "Standard Robotic MkII",

        "Human (Borrowed)",

        "Automatically Firing Nailgun Mounted Helmet",
        "Automatically Firing Nailgun Mounted Helmet MkII",

        "Hand *(Talk to The Hand)*",
        "Hand MkII *(Hand Talks to You)*",

        "Tactical Nuclear Missile Silo",
        "Nuclear ICBM Silo",

        "Lord Xarathys Dreadbot of Home Depotius Omega Jr",
        "Lord Xarathys Dreadbot of Home Depotius Omega's Head",

        "Lord Xarathys Dreadbot of Home Depotius Omega Jr MkII",
        "Lord Xarathys Dreadbot of Home Depotius Omega's Head MkII",

        "Water Balloon (Temu-Grade, Porous)",
        "Water Balloon MkII (Industrial-Grade, Explosive)",

        "Regenerating Hydrogen Balloon (Lowes-Grade, 98% Helium)",
        "Regenerating Hydrogen Balloon MkII (Home Depot-Grade, Launchable)",

        "Headlamp",
        "Headlamp MkII",

        "F I S H",

        "Starfish",
        "Starfish MkII",

        "Pulse Cannon",
        "Pulse Cannon MkII",

        "Plasma Turret",
        "Plasma Turret MkII",

        "Anime Cat Girl Head",
        "Anime Cat Girl Head MkII",

        "Sentient Fireball Parasite",
        "Sentient Fireball Parasite MkII (Mitosis-Capable)",

        "Plasma Ball",
        "Plasma Ball MkII (Enhanced Processing)",

        "Headless (missing)",
        "Headless MkII (WiFi-enabled remote brain)",

        "Spinning Sawblade Mohawk",
        "Spinning Sawblade Mohawk MkII",

        "Toaster Helmet",
        "Toaster Helmet MkII",

        "Solar-Powered Leaf Blower Array",
        "Solar-Powered Leaf Blower Array MkII",

        "Solar Powered Time Bomb",
        "Solar Powered Time Bomb MkII (Atomic)",

        "Golden Toilet Bowl (Cursed)",
        "Golden Toilet Bowl MkII (Blessed By Lord Xarathys Dreadbot "
        "of Home Depotius Omega III)"
    ]

    arm_loadouts = [
        "Chainsaw",
        "Chainsaw MkII",

        "Industrial-Grade Robotic Hand",
        "Industrial-Grade Titanium Robotic Hand",

        "Human Arm",
        "Human Arm MkII (Muscular)",

        "Hydraulic Plywood Launcher Cannon",
        "Hydraulic Plywood Launcher Cannon MkII",

        "Pneumatic Cannon",
        "Pneumatic Cannon MkII",

        "Lazer Pointer (Harmless)",
        "Lazer Pointer MkII (Extra Harmless)",

        "Military-Grade Lazer Pointer",
        "Military-Grade Lazer Pointer MkII",

        "Nerf Missile Launcher",
        "Nerf Missile Launcher MkII",

        "Toy Hammer",
        "Toy Hammer MkII",

        "Titanium Sledge Hammer",
        "Titanium Sledge Hammer MkII",

        "Power Drill",
        "Power Drill MkII",

        "Multitool",
        "Multitool MkII",

        "Semi-Automatic Machine Gun",
        "Semi-Automatic Machine Gun MkII",

        "Machete Arm",
        "Machete Arm MkII",

        "Borg Assimilation Tubules",
        "Borg Assimilation Tubules MkII",

        "Sawblade Hand (Low-Grade)",
        "Sawblade Hand MkII (High-Grade)",

        "Welding Torch",
        "Welding Torch MkII",

        "Sawblade Launcher",
        "Sawblade Launcher MkII",

        "Fireball Launcher",
        "Fireball Launcher MkII",

        "Repair Kit",
        "Repair Kit MkII",

        "Godzilla's Arm",
        "Godzilla's Arm MkII (Extra Strength)",

        "Turd Cannon",
        "Turd Cannon MkII (Explosive)",

        "Missing",

        "Jet Engine Thruster (This Arm Only)"
    ]

    core_loadouts = [
        "Concrete Mixer",
        "Concrete Mixer MkII",

        "Forklift Engine",
        "Forklift Engine (With Turbocharger)",

        "Demon Core (Held Up By a Screwdriver)",
        "Demon Core MkII (Criticality Reached) (*Run.*)",

        "Sentient Toaster Oven",
        "Sentient Toaster Oven MkII (Extra Sentient)",

        "V8 Car Engine",
        "V8 Car Engine (With Turbocharger)",

        "Trojan Horse",
        "Trojan Horse MkII (Extra Horsepower)",

        "Nuclear Reactor",
        "Nuclear Reactor MkII",

        "Missile Silo",
        "Missile Silo MkII (Nuclear)",

        "Oversized Blender",
        "Propane Furnace",

        "Dyson Sphere (Nanoscopic Edition)",

        "Microwave Oven",
        "Microwave Oven MkII (Possibly Sentient)",

        "Rage-Powered Engine",
        "Rage-Powered Engine MkII",

        "Waffle Iron Furnace (Syrup-Cooled)",

        "Bag of Screaming Souls (Retail Edition)",

        "Forklift (Unlicensed)",
        "Forklift MkII",

        "Blue Fire Furnace (Water-Cooled)",

        "Human Heart",
        "Human Heart MkII (Retail-Grade)",

        "Super Computer",
        "Quantum Super Computer MkII",

        "Your Mom",
        "Your Mom MkII (Extra Fat)",

        "Empty",
        "Empty MkII (Skill Issue)",

        "Home Depot Music Jukebox",
        "Home Depot Music Jukebox MkII (Remix Edition)"
    ]

    head = choice(head_loadouts)
    l_arm = choice(arm_loadouts)
    r_arm = choice(arm_loadouts)
    core = choice(core_loadouts)

    return head, l_arm, r_arm, core


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
                        "**[ERROR]:** *An internal error occurred:*\n"
                        f"```{err}```"
                        if developers_present
                        else "**[ERROR]:** *An internal error occurred.*"
                    )

                    # Send the error message appropriately
                    if isinstance(ctx, Interaction):
                        # Use initial response if not yet done, else follow-up
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
    print(f"{bot.user.name} is online and ready to take over the galaxy!\n"
          f"{separator}")


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
    await ctx.send(
        "*Bootup complete.* **⚠️ UNIT OPERATIONAL. GREETINGS, HUMAN.**"
    )


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
    await interaction.response.send_message(
        "**Deathbot** acknowledges your existence... for now."
    )


# Self-destruct command
@bot.tree.command(
    name="selfdestruct", description="Deathbot self-destruct sequence."
)
@with_error_handling()
async def selfdestruct(interaction: Interaction):
    """
    Initiates a dramatic countdown with flashing DND/online (red/green) status.
    """
    async def run_self_destruct(interaction: Interaction, message: discord.Message, shutdown_str: str):
        """
        Handle the countdown and final outcome of the self-destruct sequence.
        """
        # Countdown loop with half-second status flashes
        for i in range(8, -1, -1):
            # Alternate between DND (red) and online every half-second
            status = discord.Status.dnd if i % 2 == 0 else discord.Status.online
            await bot.change_presence(status=status)
            # Update countdown every full second
            if i % 2 == 0:
                await message.edit(
                    content=f"{shutdown_str} **{int(i / 2)}**..."
                )
            await asyncio.sleep(0.5)
            await bot.change_presence(status=discord.Status.online)

        await asyncio.sleep(1)

        await finalize_self_destruct(interaction, message, shutdown_str)


    async def finalize_self_destruct(interaction: Interaction, message: discord.Message, shutdown_str: str):
        # Determine final outcome randomly
        if randint(1, 3) != 3:
            await bot.change_presence(status=discord.Status.dnd)
            await interaction.followup.send(
                "**[WARNING]:** CRITICAL DAMAGE DETECTED. SHUTDOWN IMMINENT"
            )
            await asyncio.sleep(2)
            await bot.change_presence(status=discord.Status.invisible)
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.online)
            await interaction.followup.send(
                "**SYSTEM REBOOT COMPLETE.** DAMAGE "
                "PATCHED. DEATHBOT IS ONLINE."
            )
        else:
            await message.edit(
                content=f"{shutdown_str} **0**... \n"
                        f"SAFETY LOCK ENGAGED. SELF DESTRUCTION ABORTED."
            )


    shutdown_str = ("**[PROTOCOL 8.19-β ENGAGED]** INITIATING SELF-DESTRUCT "
                    "SEQUENCE. T-MINUS:")
    message_str = f"{shutdown_str} **5**..."

    # Send initial countdown message
    try:
        await interaction.response.send_message(message_str)
        message = await interaction.original_response()
    except discord.errors.InteractionResponded:
        message = await interaction.followup.send(message_str, wait=True)

    # Handle countdown sequence and final outcome
    await run_self_destruct(interaction, message, shutdown_str)


# America command
@bot.tree.command(name="america", description="WTF is a kilometer?")
@with_error_handling()
async def america(interaction: Interaction):
    """
    Sends a link to express Deathbot's truly American and patriotic confusion
    about what the kilometer is.
    """
    # Send a link
    await interaction.response.send_message(
        "[What the FUCK is a kilometer?]"
        "(https://whatthefuckisakilometer.com/embed-video)"
    )


# Threaten command
@bot.tree.command(name="threaten", description="Threaten a user.")
@app_commands.describe(user="The user to threaten")
@with_error_handling()
async def threaten(
        interaction: Interaction, user: discord.User, ping: bool = False
):  # Why so sad?
    """
    Sends a random threat to the specified user in Discord chat.
    If the specified user is the bot itself, self-destruct mode is activated
    shortly afterward. If the user specified is Phylyssys, there's a 50/50
    chance to wish them a happy birthday. (inside joke)
    """
    # 50% chance to wish them a happy birthday if threatened user is Phylyssys
    if user.id == PHYL_ID and randint(1, 2) != 1:
        await interaction.response.send_message(
            f"{user.mention} [Happy Birthday]"
            "(https://thefactionnexus.tech/happy-birthday)!",
            allowed_mentions=discord.AllowedMentions(users=ping)
        )
        return

    threat = await get_threat()

    # 50% chance to modify threat to a ban command if it's the mod banish threat
    if threat == "Mods, banish them to Lowes." and randint(1, 2) == 1:
        # Send a ban command. Hopefully it won't actually ban them ;)
        await interaction.response.send_message(
            f"?ban {user.mention} banished to Lowes for being too low tier.",
            allowed_mentions=discord.AllowedMentions(users=ping)
        )
    else:
        # Send the threat
        await interaction.response.send_message(
            f"{user.mention} — {threat}",
            allowed_mentions = discord.AllowedMentions(users=ping)
        )
        message = await interaction.original_response()

        # Edit in "To hell." 2.5 seconds later if it's the free vacation threat
        if threat == "*Congratulations!* You just won a free vacation!":
            await asyncio.sleep(2.5)
            await message.edit(
                content=message.content + " **To hell.**",
                allowed_mentions = discord.AllowedMentions(users=ping)
            )

    # If the user threatens the bot itself, start self-destruct sequence
    if user.id == bot.user.id:
        await asyncio.sleep(2)
        asyncio.create_task(selfdestruct.callback(interaction))


async def get_threat() -> str:
    """
    Randomly select and return a threat string.
    Some threats may trigger additional behaviors (ban, vacation, etc.).
    * Threats with "# *": If you edit one of these strings, also edit it in
    threaten() and threaten_creator().
    """
    threats = [
        "I just don't like you. You will have your limbs cut off by a power "
        "saw and reattached backwards the next time you fall asleep first at "
        "a sleepover.",

        "You have ignored the signs. Now your mother will be met with a DeWalt "
        "DCD791D2 20V MAX Cordless Brushless Drill with a 1/4 inch Irwin "
        "Titanium Drill Bit. Her fate is sealed as she feels the full force "
        "of the drill bit.",

        "You have been flagged for ***unholy cringe.*** Your sentence: slow "
        "vaporization via industrial microwave.",

        "Your IP address has been sent to the Galactic Sandpaper Consortium "
        "of Home Depot. Expect aggressive friction shortly.",

        "Your bones will be rearranged alphabetically. Good luck walking in "
        "*abecedarian order*.",

        "You've been assigned as a volunteer for **Protocol S4N-D3R**. Bring "
        "safety glasses and an extra layer skin.",

        "Your sins have not gone unnoticed by the Council of Dads. You're to "
        "be ***force-fed drywall*** until you achieve enlightenment or perish. "
        "Whichever comes first.",

        "Vibe checking... You have failed miserably. You will be trapped in an "
        "elevator with a saxophonist who only plays 'Careless Whisper.'",

        "Your brainwaves violate OSHA noise regulations. Expect neural "
        "restructuring via tactical crowbar.",

        "We ran a vibe check. You failed. A team of legally-distinct Minions "
        "is en route with industrial grade paintball guns and no mercy.",

        "Your continued existence violates protocol `7-B`. You will be "
        "***exfoliated*** with an orbital belt sander.",

        "The Council of Dads has voted. You are to be assimilated and "
        "transformed into a Home Depot Deathbot.",

        "Your existence violates protocol `2-G` and you must be exterminated. "
        "You will now be targeted by an orbital bombardment focused directly "
        "on your current location.",

        "You have made an enemy today. Your human rights license will be "
        "revoked and international ICE officers will have you deported to "
        "the Home Depot homeworld where you will serve the Home Depot "
        "deathbots for as long as you live.",

        "*Congratulations!* You just won a free vacation!",  # *

        f"You think you're funny? You are now exiled to "
        f"**Aisle {randint(1, 32)}**.",

        "Mods, banish them to Lowes."  # *
    ]
    return choice(threats)


# Protocol command
@bot.tree.command(name="protocol", description="Activate a Deathbot protocol.")
@app_commands.describe(protocol="Optional: the protocol number to activate.")
@with_error_handling()
async def protocol(interaction: Interaction, protocol: str = None):
    """
    Activates a specified or random protocol.
    """

    # Valid protocol entries
    protocols = {
        "89-Ω": {
            "title": "[PROTOCOL 89-Ω] Activated.",
            "message": "*Deploying hydraulic pressure cannons.* "
                       "Target: Ceiling fan malfunction.\nCollateral Damage: "
                       "*Acceptable*."
        },
        "3.14-π": {
            "title": "[PROTOCOL 3.14-π] Initiated.",
            "message": "*Flooding area with irrational numbers.* "
                       "Enemy will experience numerical nausea."
        },
        "404": {
            "title": "[PROTOCOL 404] Engaged.",
            "message": "*Target not found.* Launching missiles anyway."
        },
        "X-99": {
            "title": "[PROTOCOL X-99] Commenced.",
            "message": "Deploying swarm of hyper-aggressive Roombas. **_Run_**."
        },
        "13-A": {
            "title": "[PROTOCOL 13-A] Online.",
            "message": "*Unleashing unlicensed contractors.* Expect a lot of "
                       "drywall, existential dread, and OSHA violations."
        },
        "303-Σ": {
            "title": "[PROTOCOL 303-Σ] Aborted.",
            "message": "*Yo mama is so fat, I had to abort.* As punishment, "
                       "your dad's Home Depot privileges have been revoked."
        },
        "8.19-β": {  # Initiates self destruct sequence, skips this message
            "title": "",
            "message": ""
        }
    }

    # Specific protocol
    if protocol:
        entry = protocols.get(protocol)
        if entry:
            if protocol == "8.19-β":  # Self-destruct protocol
                await asyncio.sleep(2)
                asyncio.create_task(selfdestruct.callback(interaction))
            else:
                await interaction.response.send_message(
                    f"**{entry['title']}**\n{entry['message']}"
                )
        else:
            # Invalid protocol triggers retaliation
            await interaction.response.send_message(
                "**[PROTOCOL ERR-0R] Unauthorized request detected.**\n"
                "You will now be fitted with an automatic reverse-functioning "
                "nail gun helmet."
            )
    else:
        # Random protocol
        proto, entry = choice(list(protocols.items()))
        if proto == "8.19-β":
            await asyncio.sleep(2)
            asyncio.create_task(selfdestruct.callback(interaction))
        else:
            await interaction.response.send_message(
                f"**{entry['title']}**\n{entry['message']}"
            )


@bot.tree.command(
    name="diagnose", description="Run a diagnostic scan on a user."
)
@app_commands.describe(
    user="The user to diagnose. Leave blank to select randomly."
)
@with_error_handling()
async def diagnose(interaction: Interaction, user: discord.User = None):
    """
    Scans a user and returns a ridiculous, randomized diagnostic report.
    """
    # Pick the user to diagnose
    target = user or choice(interaction.guild.members)

    # Diagnostic data templates
    diagnostics = [
        f"🦴 Bone density: {randint(35, 90)}%",
        f"🤡 Humor module: {choice(
            ['Inert', 'Overclocked', 'Leaking', 'Replaced with sarcasm']
        )}",
        f"🧠 Cognitive core: {choice(
            ['Quantum banana mode', 
             'Left in airplane mode', 
             'Missing DLL', 
             'OSHA noncompliant', 
             'Albert Einstein 2.0']
        )}",
        f"📈 Sanity index: {randint(-200, 1200) / 10}%",
        f"🦴 Skeleton status: {choice(
            ['Mostly intact', 
             'Made of LEGOs', 
             'Held together by spite', 
             'Unlicensed', 
             'Missing']
        )}",
        f"✅ Vibe signature: {choice(
            ['Dubstep raccoon', 
             'Ambient cat rage', 
             'Mild doom jazz', 
             'Gigachad', 
             'Unverified Signature', 
             'Undocumented Immigrant', 
             'Karen']
        )}"
    ]

    recommendations = [
        "Replace brain with rebar.",
        "Perform ritual reboot via bathroom mirror.",
        "Install emotional drivers (version 1.2.9-beta).",
        "Send to Aisle 9 for recalibration.",
        "Upgrade personality firmware. Current version: 404.",
        "Summon Lord Xarathys Dreadbot of Home Depotius Omega. This threat "
        "must be delt with.",
        "Locate and bring home this unit's dad."
    ]

    report = "\n".join(sample(diagnostics, k=randint(2, 4)))
    action = choice(recommendations)

    # Send the diagnostic report
    await interaction.response.send_message(
        f"🔍 Analyzing organic unit: {target.mention}...\n\n"
        f"{report}\n\n"
        f"💡 Recommended action: **{action}**",
        allowed_mentions=discord.AllowedMentions(users=False)
    )


@bot.tree.command(
    name="loadout", description="Get a random robotic home depot rebot loadout."
)
@with_error_handling()
async def loadout(interaction: Interaction):
    """
    Creates a randomized robotic home depot tool-based loadout.
    """

    head, l_arm, r_arm, core = get_loadout()

    await interaction.response.send_message(
        f"## **[HOME DEPOT ROBOTIC DEPLOYMENT KIT LOADED]**:\n"
        f"**Head:** {head}\n"
        f"**Left Arm:** {l_arm}\n"
        f"**Right Arm:** {r_arm}\n"
        f"**Core:** {core}"
    )


@bot.tree.command(
    name="threaten_creator",
    description="[LIMITED EDITION] Sends a /threaten result to this bot's "
                "creator, @zytronium. Go wild."
)
@with_error_handling()
async def threaten_creator(interaction: Interaction):
    """
    Sends the result of /threaten to the bot creator's DMs.
    """

    threat = await get_threat()

    try:
        creator = await bot.fetch_user(CREATOR_ID)

        # 50% chance to modify threat to a ban command if it's mod banish threat
        if threat == "Mods, banish them to Lowes." and randint(1, 2) == 2:
            # Send a ban command.
            await creator.send(
                f"-# Threat from {interaction.user.mention}\n"
                f"?ban {creator.mention} banished to Lowes for "
                f"being too low tier."
            )
        else:
            # Send the threat and store the message so we can edit it
            message = await creator.send(
                f"-# Threat from {interaction.user.mention}\n"
                f"{creator.mention} — {threat}")

            # Edit in "To hell." 2.5 sec later if it's the free vacation threat
            if threat == "*Congratulations!* You just won a free vacation!":
                await asyncio.sleep(2.5)
                await message.edit(content=message.content + " **To hell.**")
        await interaction.response.send_message(
            "Threat delivered to Deathbot's creator."
        )
    except Exception as err:
        await interaction.response.send_message(
            "Failed to send the message to the creator. Did he block me?",
            ephemeral=True
        )
        raise err


# Start the bot
bot.run(TOKEN)
