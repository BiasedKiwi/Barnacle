# pylint: disable=unused-argument
import discord
from discord import app_commands
from discord.ext import commands
from barnacle import PrettyPrinter


class Refresh(discord.ui.View):
    def __init__(self, bot: commands.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @discord.ui.button(label="Refresh", emoji="🔄", custom_id="barnacle_ping_cmd_button:refresh")
    async def refresh(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.message.edit(
            embed=discord.Embed(
                title="Pong!",
                description=f"The bot's current latency is {round(self.bot.latency * 1000, 1)}ms",
                color=discord.Color.gold(),
            ).set_footer(
                text=f"Refreshed by {interaction.user}",
                icon_url=interaction.user.avatar,
            )
        )
        await interaction.response.send_message("Refreshed!", ephemeral=True)


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.pretty_print = PrettyPrinter()
        print("Misc cog is ", end="")
        self.pretty_print.green("online")

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.channel.send("Synced!")

    @sync.error
    async def sync_handler(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.errors.NotOwner):
            await ctx.channel.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="Only the owner of the bot can execute this command!",
                    color=discord.Color.gold(),
                )
            )

    @app_commands.command(
        name="ping", description="Get the bot's latency in milliseconds."
    )
    async def test(self, interaction: discord.Interaction):
        view = Refresh(self.bot, timeout=None)
        embed = discord.Embed(
            title="Pong!",
            description=f"The bot's current latency is {round(self.bot.latency * 1000, 1)}ms",
            color=discord.Color.gold(),
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar
        )
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot), guilds=[discord.Object(id=883413709031108608)])
