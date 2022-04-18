import discord
from discord.ext import commands
from barnacle import PrettyPrinter


class EventListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.pretty_print = PrettyPrinter()
        print("Event Listener cog is ", end="")
        self.pretty_print.green("online")

    @commands.Cog.listener()
    async def on_connect(self):
        print("--------------------------------------------")
        print("Established connection to Discord servers.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("\nLogged in as ", end="")
        self.pretty_print.bold(str(self.bot.user))
        print(f"ID: {self.bot.user.id}")
        self.pretty_print.bold("Barnacle is online and connected to Discord.")

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id: int):
        print(f"Shard {shard_id} connected.")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        EventListener(bot), guilds=[discord.Object(id=883413709031108608)]
    )
