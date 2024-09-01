import discord

from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        data = self.bot.get_cog("GuildInfo")
        cmd = data.get_control_message(payload.guild_id)

        if cmd is None:
            return

        if payload.emoji.name == "⏹️":
            audio = self.bot.get_cog("PlayAudio")
            await audio.leave_channel(payload.guild_id)
        elif payload.emoji.name == "⏭️":
            audio = self.bot.get_cog("PlayAudio")
            await audio.stop_audio(payload.guild_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, user: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if user != self.bot.user:
            return

        if before.channel is not None and after.channel is None:
            data = self.bot.get_cog("GuildInfo")
            data.remove_control_message(user.guild.id)


async def setup(bot: commands.Bot):
    await bot.add_cog(Listeners(bot))
