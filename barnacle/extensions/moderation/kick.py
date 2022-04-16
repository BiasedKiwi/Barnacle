import discord
from discord.ext import commands
from discord import Color as color
from barnacle import PrettyPrinter

class Kick(commands.Cog):
    """The kick command."""
    def __init__(self, bot: commands.Bot):
        self.pretty_print = PrettyPrinter()
        print("Kick command is ", end="")
        self.pretty_print.green("online")
        self.bot = bot
        
    @commands.command(name="kick", description="Kick a user from the server.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Kick a user from the server."""
        if reason is None:
            reason = "No reason provided."
        await member.kick(reason=reason)
        await ctx.channel.send(embed=discord.Embed(title="Done!", description=f"{member.mention} has been kicked.", color=color.gold()))

    @kick.error
    async def kick_handler(self, ctx: commands.Context, error: commands.CommandError):
        """The error handler for the kick command"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title="Something went wrong!", description="You do not have permission to kick users.", color=color.gold()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="Something went wrong!", description="You need to specify a user to kick.", color=color.gold()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title="Something went wrong!", description="The user you specified does not exist.", color=color.gold()))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=discord.Embed(title="Something went wrong!", description="I do not have permission to kick users.", color=color.gold()))
        else:
            raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))