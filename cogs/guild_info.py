import discord
import asyncio

from discord.ext import commands
from collections import defaultdict
from typing import Union


class GuildInfo(commands.Cog):
    guild_queues = defaultdict(list)
    guild_control_messages = {}

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    def get_queue(self, guild_id: int):
        return self.guild_queues[guild_id]

    def add_queue(self, guild_id: int, info: dict):
        self.guild_queues[guild_id].append(info)

    def next_queue(self, guild_id: int) -> Union[dict, None]:
        if self.len_queue(guild_id) == 0:
            return None

        return self.guild_queues[guild_id].pop(0)

    def len_queue(self, guild_id: int) -> int:
        return len(self.guild_queues[guild_id])

    def get_control_message(self, guild_id: int):
        return self.guild_control_messages.get(guild_id, None)

    def set_control_message(self, guild_id: int, ctx: discord.WebhookMessage):
        if guild_id in self.guild_control_messages:
            self.remove_control_message(guild_id)

        self.guild_control_messages[guild_id] = ctx
        asyncio.run_coroutine_threadsafe(
            self.add_control_reactions(ctx), self.bot.loop)

    def remove_control_message(self, guild_id: int):
        if guild_id not in self.guild_control_messages:
            return

        asyncio.run_coroutine_threadsafe(
            self.guild_control_messages[guild_id].clear_reactions(), self.bot.loop)
        del self.guild_control_messages[guild_id]

    async def add_control_reactions(self, ctx: discord.WebhookMessage):
        await ctx.add_reaction("⏹️")
        await ctx.add_reaction("⏭️")


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildInfo(bot))
