import discord

from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @discord.app_commands.command(name="sync")
    async def sync(self, ctx: discord.Interaction):
        if self.bot.admin_id is None or ctx.user.id != self.bot.admin_id:
            await ctx.response.send_message("You are not allowed to use this.", ephemeral=True)
            return

        await self.bot.tree.sync()

        await ctx.response.send_message("Commands synced.", ephemeral=True)

    @discord.app_commands.command(name="reload")
    async def reload(self, ctx: discord.Interaction):
        if self.bot.get_extensions is None or ctx.user.id != self.bot.admin_id:
            await ctx.response.send_message("You are not allowed to use this.", ephemeral=True)
            return

        for ext in self.bot.get_extensions():
            try:
                await self.bot.reload_extension(ext)
            except commands.ExtensionNotLoaded:
                await self.bot.load_extension(ext)
            except Exception as e:
                print(e)

        await ctx.response.send_message("Extensions reloaded.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))
