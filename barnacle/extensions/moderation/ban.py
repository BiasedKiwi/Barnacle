import discord
from barnacle import PrettyPrinter
from discord import Color as color
from discord.ext import commands


class Ban(commands.Cog):
    """The ban command."""
    def __init__(self, bot: commands.Bot):
        self.pretty_print = PrettyPrinter()
        print("Ban command is ", end="")
        self.pretty_print.green("online")
        self.bot = bot
        
    @commands.command(name="ban", description="Permanently ban a user from the server.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Ban a user from a server."""
        if reason is None:
            reason = "No reason provided."
        await member.ban(reason=reason)
        await ctx.channel.send(embed=discord.Embed(title="Done!", description=f"{member.mention} has been kicked.", color=color.gold()))
        
    @ban.error
    async def ban_handler(self, ctx: commands.Context, error: commands.CommandError):
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
        
def setup(bot: commands.Bot):
    bot.add_cog(Ban(bot))
