import discord
from discord import Color as color
from discord import app_commands
from discord.ext import commands
from barnacle import PrettyPrinter


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.confirmed = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("Confirmed!", ephemeral=True)
        self.confirmed = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelled.", ephemeral=True)
        self.confirmed = False
        self.stop()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.pretty_print = PrettyPrinter()
        print("Moderation cog is ", end="")
        self.pretty_print.green("online")

    @app_commands.command(name="kick", description="Kick a user from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.describe(
        member="The member to kick.", reason="Why do you want to kick this user?"
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        """Kick a user from the server."""
        if reason is None:
            reason = "No reason provided."
        try:
            await member.kick(reason=reason)
        except Exception as e:
            embed = discord.Embed(
                title="Something went wrong!",
                description=f"Something went wrong while trying to kick {member}, make sure they are not a bot.",
                color=color.gold(),
            )
            embed.add_field(name="Debug info", value=f"```{e}```")
            await interaction.response.send_message(embed=embed)
            return
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Done!",
                description=f"{member.mention} has been kicked.",
                color=color.gold(),
            )
        )

    @kick.error
    async def kick_handler(self, ctx: commands.Context, error: commands.CommandError):
        """The error handler for the kick command"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="You do not have permission to kick users.",
                    color=color.gold(),
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="You need to specify a user to kick.",
                    color=color.gold(),
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="The user you specified does not exist.",
                    color=color.gold(),
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="I do not have permission to kick users.",
                    color=color.gold(),
                )
            )
        else:
            raise error

    @app_commands.command(
        name="ban", description="Permanently ban a user from the server."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to ban.", reason="Why do you want to ban this user?"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        """Ban a user from a server."""
        if reason is None:
            reason = "No reason provided."
        await member.ban(reason=reason)
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Done!",
                description=f"{member.mention} has been banned.",
                color=color.gold(),
            )
        )

    @app_commands.command(name="unban", description="Unban a user from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        member_id="The ID of the user you would like to unban from the server."
    )
    async def unban(
        self, interaction: discord.Interaction, member_id: int
    ):  # TODO: Make this command support using usernames.
        """unban a user from a server."""
        if member_id is not None:
            try:
                user: discord.User = await self.bot.fetch_user(member_id)
                await interaction.guild.unban(user)
            except discord.NotFound:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Something went wrong!",
                        description="The user ID you specified does not exist or isn't banned.",
                        color=color.gold(),
                    )
                )
                return
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Done!",
                    description=f"Successfully unbanned {user.name} with ID {user.id}.",
                    color=color.gold(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="You need to specify a user ID to unban.",
                    color=color.gold(),
                )
            )

    @unban.error
    @ban.error
    async def ban_handler(self, ctx: commands.Context, error: commands.CommandError):
        """The error handler for the kick command"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Something went wrong!",
                description="You do not have permission to kick users.",
                color=color.gold(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Something went wrong!",
                description="You need to specify a user to kick.",
                color=color.gold(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Something went wrong!",
                description="The user you specified does not exist.",
                color=color.gold(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Something went wrong!",
                description="I do not have permission to kick users.",
                color=color.gold(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NoPrivateMessage):
            embed = discord.Embed(
                title="Something went wrong!",
                description="You cannot use this command in DMs",
                color=color.gold(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
        else:
            raise error

    @app_commands.command(
        name="purge",
        description="Delete a number of messages from the current channel.",
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(number_of_messages="The number of messages to delete.")
    async def purge(self, interaction: discord.Interaction, number_of_messages: int):
        if number_of_messages >= 100:
            view = Confirm()
            await interaction.response.send_message(
                f"Are you sure you want to delete {number_of_messages} messages?",
                view=view,
            )
            await view.wait()
            if view.confirmed is None:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Cancelled!", description="Timed out.", color=color.gold()
                    )
                )
            elif view.confirmed:
                await interaction.channel.purge(limit=number_of_messages)
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Done!",
                        description=f"Deleted {number_of_messages} messages.",
                        color=color.gold(),
                    )
                )
            elif not view.confirmed:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="Got it!",
                        description=f"Cancelled the deletion of {number_of_messages} messages.",
                        color=color.gold(),
                    )
                )
        else:
            await interaction.channel.purge(limit=number_of_messages)
            await interaction.response.send_message(
                "Deleted {} messages.".format(number_of_messages)
            )

    @purge.error
    async def purge_handler(self, ctx: commands.Context, error: commands.CommandError):
        """The error handler for the kick command"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="You do not have permission to delete messages.",
                    color=color.gold(),
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="I do not have permission to delete messages.",
                    color=color.gold(),
                )
            )
        else:
            raise error

    @app_commands.command(
        name="mute", description="Permanently mute a user from the server."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(member="The member to mute.")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = "No reason provided."
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await interaction.guild.create_role(name="Muted", colour=color.gold())
        perms = discord.Permissions(send_messages=False)
        guild = interaction.guild
        categories =  discord.utils.get(guild.categories)
        await categories.set_permissions(guild.default_role, send_messages=None)
        await categories.set_permissions(muted_role, send_messages=False)
        embed = discord.Embed(title="User muted", description=f"{member} was muted", colour=color.gold())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        await member.add_roles(muted_role, reason=reason)
        await member.send(f"You have been muted from {guild.name}. Reason: {reason}")

    @app_commands.command(name="unmute", description="Unmute a user from the server.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(member="The member to unmute.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if member.guild._roles.get("Muted") is None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="The user isn't muted!",
                    color=color.gold(),
                )
            )
        try:
            await member.remove_roles(
                discord.utils.get(member.guild.roles, name="Muted")
            )
        except (discord.errors.NotFound, AttributeError) as e:
            await interaction.response.send_message(
                discord.Embed(
                    title="Something went wrong!",
                    color=color.gold(),
                ).add_field(name="Debug Info", value=e)
            )
            return

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Done!",
                description=f"Successfully unmuted {member.mention}.",
                color=color.gold(),
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot), guilds=[discord.Object(id=883413709031108608)])
