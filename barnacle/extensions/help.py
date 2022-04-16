import discord
from discord import Color as color
from discord.ext import commands
from barnacle import PrettyPrinter


class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            await destination.send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.pretty_print = PrettyPrinter()
        print("Help cog is ", end="")
        self.pretty_print.green("online")
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
