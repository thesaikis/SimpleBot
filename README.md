# SimpleBot
This is a simple discord bot which is able to stream audio to a voice channel. Follow the instructions below if you want to set it up for your own machine. It is built using cogs and should be easily extensible.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine using:

```bash
git clone git@github.com:thesaikis/SimpleBot.git
cd SimpleBot
```

### 2. Create a `.env` File

Create a `.env` file in the root directory of the project. This file will store your Discord bot token.
```bash
touch .env
```

Add the following line to you `.env` file:
```
DISCORD_KEY=your_discord_bot_token_here
```
Replace `your_discord_bot_token_here` with your actual Discord bot token.

> [!WARNING]
> __Warning__: DO NOT share your Discord bot token. Anyone with access to the token can use your bot in any way they want.

### 3. Add a `cookies.txt` File

If you want to be able to use the audio streaming feature, you may need a `cookies.txt` file. This file should contain the cookies required for any web scraping or API requests your bot might need.

> [!WARNING]
> __Warning__: DO NOT share your cookies file! This can include sensitive information and if shared may allow people to access your accounts. I will not share how to obtain this file. It is your responsibility to understand the risks and understand what you're doing.

### 4. Install Dependencies
Install the necessary Python packages:
```bash
pip install -r requirements.txt
```

### 5. Run the Bot
You can run the bot in the background using:
```bash
./start.sh
```

Or, alternatively:
```bash
python3 main.py
```
