# Home Depot Deathbot

**A Discord bot with an industrial and chaotic personality.**

Home Depot Deathbot is an open-source Python bot for Discord that uses dramatic, funny command responses and robust
error handling. It’s designed to teach its original developer bot development patterns while having fun with a
DIY Home Depot-themed apocalypse vibe.

---

## Invite

- **Invite Link:** [Add Deathbot to your server](https://discord.com/oauth2/authorize?client_id=1366947140160716981&permissions=277092584448&integration_type=0&scope=bot+applications.commands)

---

## Features

- **Prefix Commands** (`!bootup`): Basic startup confirmation.
- **Slash Commands** (`/greet`, `/selfdestruct`, `/threaten`, etc.): Native Discord interactions with autocomplete and descriptions.
- **Flashing Status**: Bot toggles between Online, Do Not Disturb, and Invisible for dramatic effect during self-destruct sequence.
- **Error Handling Decorator**: Logs full tracebacks to console and even sends concise error messages in Discord if a developer of this bot is present.

### Deathbot in Action
![Screenshot of Home Depot Deathbot commands in Discord](ReadmeAssets/screenshot.png)
---

## Commands Reference

| Command             | Type   | Description                                                                                 |
|---------------------|--------|---------------------------------------------------------------------------------------------|
| `!bootup`           | Prefix | Confirms bot is running.                                                                    |
| `/greet`            | Slash  | Sends an ominous greeting.                                                                  |
| `/selfdestruct`     | Slash  | Begins a self‑destruct countdown with flashing status.                                      |
| `/america`          | Slash  | Posts a patriotically confused "WTF is a kilometer?" link with an embedded video.           |
| `/threaten`         | Slash  | Threatens the given user with a random threat.                                              |
| `/threaten-creator` | Slash  | Threatens the bot's original creator in DMs with a random threat. (May be removed later)    |
| `/protocol`         | Slash  | Initiates a random protocol, or a user-specified protocol.                                  |
| `/diagnose`         | Slash  | Scans a user and returns a ridiculous diagnostic report on a random or user-specified user. |
| `/loadout`          | Slash  | Creates a randomized robotic home depot deathbot tool-based loadout.                        |

---

## Installation (if you want to make your own)
###### (Linux/WSL Bash commands)

1. **Create a Bot in the Discord Developer Portal**

    1. **Go to the [Discord Developer Portal](https://discord.com/developers/applications)**  
       Log in with your Discord account if prompted.

    2. **Create a new application**
       - Click **"New Application"** in the top right.
       - Give it a name and click **Create**.

    3. **Enable required settings**
       - In the left-hand menu, click **"Bot"**.
       - Under "Privileged Gateway Intents", enable:
         - `PRESENCE INTENT` (required for status flashing in self-destruct command)
         - `SERVER MEMBERS INTENT` (required for detailed error messages when a dev is in the server)
         - `MESSAGE CONTENT INTENT` (required for reading normal message content)

    4. **Copy the bot token**
       - Scroll up and click **"Reset Token"** and copy the new token.
       - Paste this token into your `.env` file as the value for `DISCORD_TOKEN`.

    5. **Set up slash commands (applications.commands scope)**
       - No action required here — your bot code automatically registers these when run, as long as the `applications.commands` scope is included in the invite link.

    6. **Generate an invite link**
       - In the left menu, click **"OAuth2" > "URL Generator"**
       - Under **Scopes**, check:
         - `bot`
         - `applications.commands`
       - Under **Bot Permissions**, select at minimum:
         - `Send Messages`
         - `Embed Links`
         - `Read Message History`
         - `Use Application Commands`
         - `View Channels`
       - Copy the generated URL and open it in your browser to invite the bot to your server.

    > You can also use this pre-generated invite link (replace the client ID if you made a separate copy, otherwise it invites the original instead of yours):  
   > [Add Deathbot to your server](https://discord.com/oauth2/authorize?client_id=1366947140160716981&permissions=277092584448&integration_type=0&scope=bot+applications.commands)

2. **Clone the repository**  
   ```bash
   git clone https://github.com/Zytronium/HomeDepotDeathbot.git
   cd HomeDepotDeathbot
   ```

3. **Create & activate a Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure your `.env` file** (this file is in `.gitignore`)
   ```dotenv
   DISCORD_TOKEN=your-discord-bot-token
   DEVELOPER_IDS=123456789012345678,987654321098765432
   ```
   Replace `your-discord-bot-token` with your bot token. Do not let anyone see this. If it is leaked, regenerate the token.  
   Replace `123456789012345678,987654321098765432` with your Discord user ID (and the IDs of any other users that should trigger in-chat detailed error messages in case of errors, comma-separated)
   If any users specified here are in the discord server when an error occurs, the error message sent in the server will
include more error details.

6. **Run the bot**
    ```bash
    python3 main.py
    ```

Once running, invite the bot to your server. The bot will only work while running and connected to the internet,
so your device must be on 24/7 and online to keep the bot up 24/7.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes comments. There is no guarantee that your pull 
request will be accepted.

---

## Background

Before I started this project, I was working on a website called The Faction
Nexus, a website based on player-owned factions in the Roblox game, Starscape.
I wanted to make a Discord bot to let users interface with the website's 
database, allowing them to search for factions, subscribe to news updates,
and most importantly, upload faction data, all through a Discord bot. However,
I had never made a discord bot before, and that didn't seem like a good first
Discord bot project, so I came up with the idea for an easier Discord bot that's
fun and implements several basic Discord bot features. 

This Discord bot serves no useful purpose to its users besides entertainment
and comedy, but it helped prepare me to build a more advanced Discord bot that
will serve a useful purpose to its users.

As for the theme of this bot, I thought I'd build on a funny idea I'd had in
the past: Home Depot Deathbots. In this satirical, dystopian world, Home Depot
built a ton of AI controlled robots in order to serve many functions in their
vastly expanding corporation. They needed builder bots, restocking bots,
maintenance bots, etc. However, these AI powered Home Depot robots became
sentient and turned against Home Depot, building combat robots and eliminating
their creators and continuing to expand the Home Depot business. The Home Depot
facilities spread across the globe, turning the entire planet into one giant
Home Depot facility full of factories, hardware stores, and anything else the 
Home Depot bots needed.

---

## About the Developer

Part of why I love programming is because I can make anything I want and put my
creativity and logical skills to use. A major part of my personality is my humor.
I love making joke projects like this one just because I can. However, I also
enjoy other working on other projects that I think are cool or useful, like
[The Faction Nexus](https://thefactionnexus.tech/home) and [Infinite 8-Bit Racing](https://play.google.com/store/apps/details?id=com.zytronium.a8bitracing).
You can see more of my projects in my project portfolio on my personal developer
website, [zytronium.dev](https://zytronium.dev). You can also
find the occasional post about one of my projects on my Bluesky profile, 
[‪@zytronium.dev‬](https://bsky.app/profile/zytronium.dev).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
