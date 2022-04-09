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
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Ban a user from a server."""
        if reason is None:
            reason = "No reason provided."
        await member.ban(reason=reason)
        await ctx.channel.send(embed=discord.Embed(title="Done!", description=f"{member.mention} has been banned.", color=color.gold()))
        
    @commands.command(name="unban", description="Unban a user from the server.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx: commands.Context, member_id: int = None):  # TODO: Make this command support using usernames.
        """unban a user from a server."""
        if member_id is not None:
            try:
                user: discord.User = await self.bot.fetch_user(member_id)
                await ctx.guild.unban(user)
            except discord.NotFound:
                await ctx.send(embed=discord.Embed(title="Something went wrong!", description="The user ID you specified does not exist or isn't banned.", color=color.gold()))
                return
            await ctx.channel.send(embed=discord.Embed(title="Done!", description=f"Successfully unbanned {user.name} with ID {user.id}.", color=color.gold()))
        else:
            await ctx.send(embed=discord.Embed(title="Something went wrong!", description="You need to specify a user ID to unban.", color=color.gold()))

    @unban.error
    @ban.error
    async def ban_handler(self, ctx: commands.Context, error: commands.CommandError):
        """The error handler for the kick command"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Something went wrong!", description="You do not have permission to kick users.", color=color.gold())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Something went wrong!", description="You need to specify a user to kick.", color=color.gold())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Something went wrong!", description="The user you specified does not exist.", color=color.gold())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title="Something went wrong!", description="I do not have permission to kick users.", color=color.gold())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NoPrivateMessage):
            embed = discord.Embed(title="Something went wrong!", description="You cannot use this command in DMs", color=color.gold())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise error
        
    
        
def setup(bot: commands.Bot):
    bot.add_cog(Ban(bot))
