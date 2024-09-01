import os

from discord.ext import commands

# Your Discord user ID here
ADMIN_USER_ID = -1


class SimpleBot(commands.Bot):
    async def on_ready(self):
        self.admin_id = ADMIN_USER_ID
        print("Logged in")

    async def setup_hook(self):
        for ext in self.get_extensions():
            await self.load_extension(ext)

    def get_extensions(self):
        cogs_folder = "cogs"
        cogs_list = []

        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                cogs_list.append(f"cogs.{filename[:-3]}")

        return cogs_list
