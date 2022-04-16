import discord
from discord import app_commands
from discord.ext import commands
from barnacle import PrettyPrinter


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.pretty_print = PrettyPrinter()
        print("Misc cog is ", end="")
        self.pretty_print.green("online")
        self.bot = bot
        
    @commands.command(name="ping", description="Get the bot's latency in milliseconds.")
    async def test(self, ctx):
        """Fetches the bot's latency in milliseconds using `self.bot.latency`."""
        embed = discord.Embed(title="Pong!", description=f"The bot's current latency is {round(self.bot.latency * 1000, 1)}ms", color=discord.Color.gold())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.channel.send("Synced!")
        
    @app_commands.command(name="ping", description="Get the bot's latency in milliseconds.")
    async def test(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Pong!", description=f"The bot's current latency is {round(self.bot.latency * 1000, 1)}ms", color=discord.Color.gold())
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot), guilds=[discord.Object(id=883413709031108608)])
