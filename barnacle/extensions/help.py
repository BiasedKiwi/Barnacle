import discord
from discord import Color as color
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        print("Help cog is online.")
        self.bot = bot

    @commands.command(name="help", description="Returns all commands available")
    async def help(self, ctx):
        """Self updating help command. It fetches all the commands using `self.bot.commands` and uses their `description` attribute as the help text."""
        embed = discord.Embed(title="Barnacle Help", description="All commands are listed below.", color=color.gold())
        for command in self.bot.commands:  # Iterate through all the registered commands
            embed.add_field(name=command.name, value=command.description, inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
