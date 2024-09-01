import discord
import importlib
import asyncio

from discord.ext import commands
from typing import Union
from concurrent.futures import ThreadPoolExecutor

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -fflags +discardcorrupt",
}


class PlayAudio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.reload_script()

        # In some cases, we may use leave_channel() directly.
        # If the bot is playing an audio, `after_audio` may be called, and then `leave_channel` again.
        # This could lead to two vc.disconnect() calls on the same vc and eventually an asyncio TimeoutError.
        # So, a lock is used to ensure we only attempt to leave once.
        self.leave_lock = asyncio.Lock()

    def reload_script(self):
        import scripts.extract_audio
        importlib.reload(scripts.extract_audio)
        self.extract_audio = scripts.extract_audio.extract_audio

    async def leave_channel(self, guild_id: int):
        async with self.leave_lock:
            vc = discord.utils.get(self.bot.voice_clients,
                               guild__id=guild_id)
            if vc is not None:
                await vc.disconnect()

    async def after_audio(self, error, voice_client: discord.VoiceClient, ctx: discord.Interaction):
        if error:
            print(error)
            await ctx.followup.send("I had a fatal error, sorry.")

        if voice_client:
            data = self.bot.get_cog("GuildInfo")

            if data.len_queue(ctx.guild_id) > 0:
                info = data.next_queue(ctx.guild_id)
                await self.play_audio(info, voice_client, ctx)
            else:
                await self.leave_channel(ctx.guild_id)

    async def stop_audio(self, guild_id: int):
        vc = discord.utils.get(self.bot.voice_clients, guild__id=guild_id)
        if vc is not None:
            vc.stop()

    async def send_queue(self, ctx: discord.Interaction):
        data = self.bot.get_cog("GuildInfo")
        if data.len_queue(ctx.guild_id) > 0:
            embed = discord.Embed(title="Current queue", description="\n".join(
                str(i + 1) + ". " + info["title"] for i, info in enumerate(data.get_queue(ctx.guild_id))), color=discord.Color.dark_green())
            await ctx.followup.send(embed=embed)

    async def play_audio(self, info: dict, vc: Union[discord.VoiceClient, None], ctx: discord.Interaction):
        embed = discord.Embed(
            title="Now playing", description=f"[{info['title']}]({info['original_url']})", color=discord.Color.green())
        embed.set_thumbnail(url=info["thumbnail"])

        if vc is None:
            vc = await ctx.user.voice.channel.connect()

        vc.play(discord.FFmpegPCMAudio(
            info["source"], **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(self.after_audio(e, vc, ctx), self.bot.loop))

        msg = await ctx.followup.send(embed=embed)
        data = self.bot.get_cog("GuildInfo")
        data.set_control_message(ctx.guild_id, msg)
        await self.send_queue(ctx)

    @discord.app_commands.command(name="play")
    async def play(self, ctx: discord.Interaction, url: str):
        if ctx.user.voice is None:
            await ctx.response.send_message("You are not in a voice channel.", ephemeral=True)
            return

        data = self.bot.get_cog("GuildInfo")

        await ctx.response.defer()

        with ThreadPoolExecutor() as pool:
            info = await self.bot.loop.run_in_executor(pool, self.extract_audio, url)
        # info = self.extract_audio(url)

        if info is None or info["source"] is None:
            await ctx.followup.send("There was an error.")
            return

        vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if vc and vc.is_playing():
            data.add_queue(ctx.guild_id, info)
            await ctx.followup.send("Added to the queue!")
            await self.send_queue(ctx)
            return

        await self.play_audio(info, vc, ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(PlayAudio(bot))
