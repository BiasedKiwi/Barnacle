# pylint: disable=unused-argument, consider-iterating-dictionary
import re
import time

import aioredis
import discord
from barnacle import PrettyPrinter
from discord import Color as color
from discord import app_commands
from discord.ext import commands, tasks

redis = aioredis.Redis(
    host="localhost",
    port=6379,
)


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

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelled.", ephemeral=True)
        self.confirmed = False
        self.stop()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.auto_unmute.start()
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
        await member.send(
            embed=discord.Embed(title="You've been banned!", color=color.gold())
            .add_field(name="Server", value=interaction.guild)
            .add_field(name="Reason", value=reason)
        )
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
        self, interaction: discord.Interaction, member_id: str
    ):  # TODO: Make this command support using usernames.
        """unban a user from a server."""
        try:
            member_id = int(member_id)  #
        except ValueError as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="You've passed an invalid user ID!",
                ).add_field(name="Debug Info", value=f"```{e}```")
            )
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
                    description=f"Successfully unbanned {user} with ID {user.id}.",
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

    @ban.error
    @unban.error
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
            else:
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
                f"Deleted {number_of_messages} messages."
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
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None,
    ):
        try:
            if reason is None:
                reason = "No reason provided."
            muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await interaction.guild.create_role(
                    name="Muted", colour=color.gold()
                )
            guild = interaction.guild
            categories = discord.utils.get(guild.categories)
            await categories.set_permissions(guild.default_role, send_messages=None)
            await categories.set_permissions(muted_role, send_messages=False)
            embed = discord.Embed(
                title="User muted",
                description=f"{member} was muted",
                colour=color.gold(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
            await member.add_roles(muted_role, reason=reason)
            await member.send(
                embed=discord.Embed(title="You've been muted!", color=color.gold())
                .add_field(name="Server", value=interaction.guild.name)
                .add_field(name="Duration", value="Permanent.")
                .add_field(name="Reason", value=reason)
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description=f"An unrecoverable error occurred while trying to ban {member.mention}.",
                    color=color.gold(),
                ).add_field(name="Debug Info", value=f"```{e}```")
            )

    @app_commands.command(
        name="tempmute", description="Temporarily mute a user from the server."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(
        duration="how long will the mute last? (E.x. 1m = 1 minute, 1h = 1 hour, 1mo = 1 month...).",
        member="The server member you would like to mute.",
    )
    async def tempmute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: str,
        reason: str,
    ):  # Prepare the forks and the knives because you're about to see some spaghetti code.
        time_in_secs = {  # Use ReGex to get the time in seconds
            re.compile(r"(\d){1,}(s)$"): 1,
            re.compile(r"(\d{1,})(m)$"): 60,
            re.compile(r"(\d{1,})(h)$"): 3600,
            re.compile(r"(\d{1,})(d)$"): 86400,
            re.compile(r"(\d{1,})(w)$"): 604800,
            re.compile(r"(\d{1,})(mo)$"): 2629800,
            re.compile(r"(\d{1,})(y)$"): 31557600,
        }

        async def translate_duration(to_seconds: str):
            for key in time_in_secs.keys():
                match = re.match(key, to_seconds)
                if match is not None:
                    try:
                        multiplier = int(match[1])
                    except ValueError as e:
                        await interaction.response.send_message(
                            embed=discord.Embed(
                                title="Something went wrong!",
                                description="The duration you provided was in incorrect format, please follow the following format: `1m: 1 minute, 1h: 1 hour, 1d: 1 day, 1w: 1 week, 1mo: 1 month, 1y: 1 year`",
                                color=color.gold(),
                            ).add_field(name="Debug Info", value=f"```{e}```")
                        )

                        return
                    return time_in_secs[key] * multiplier
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="The duration you provided was in incorrect format, please follow the following format: `1m: 1 minute, 1h: 1 hour, 1d: 1 day, 1w: 1 week, 1mo: 1 month, 1y: 1 year`",
                    color=color.gold(),
                )
            )
            raise ValueError(key)

        async def gen_mute_entry(
            duration: int, member: discord.Member, guild: discord.Guild
        ):
            return {
                "member_id": member.id,
                "server_id": guild.id,
                "starts_at": round(time.time()),
                "ends_at": round(time.time()) + duration,
                "duration": duration,
            }

        mute_entry = await gen_mute_entry(
            await translate_duration(duration), member, interaction.guild
        )

        if reason is None:
            reason = "No reason provided."
        muted_role = discord.utils.get(
            interaction.guild.roles, name="Muted"
        )  # Create the muted role if it doesn't exist.
        if not muted_role:
            muted_role = await interaction.guild.create_role(
                name="Muted", colour=color.gold()
            )
        guild = interaction.guild
        categories = discord.utils.get(guild.categories)
        await categories.set_permissions(guild.default_role, send_messages=None)
        await categories.set_permissions(muted_role, send_messages=False)

        await redis.hset(f"mute_{guild.id}-{member.id}", mapping=mute_entry)

        embed = discord.Embed(
            title="User muted",
            description=f"{member} was muted",
            colour=color.gold(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(muted_role, reason=reason)
        await member.send(
            embed=discord.Embed(title="You've been muted!", color=color.gold())
            .add_field(name="Server", value=interaction.guild.name)
            .add_field(
                name="Duration",
                value=f"{time.strftime('%d days, %H hours, %M minutes, %M seconds', time.gmtime(await translate_duration(duration)))}",
            )
            .add_field(name="Reason", value=reason)
        )

    @tasks.loop(seconds=5)
    async def auto_unmute(self):
        def get_member_from_server(server_id: int, member_id: int):
            guild = self.bot.get_guild(server_id)
            return (guild, guild.get_member(member_id))

        scan = await redis.scan(cursor=0, match="mute_*")
        for key in scan[1]:
            table = await redis.hgetall(key)
            if int(table[b"ends_at"]) < round(time.time()):
                instance_objects = get_member_from_server(
                    int(table[b"server_id"]), int(table[b"member_id"])
                )
                await instance_objects[1].remove_roles(
                    discord.utils.get(instance_objects[0].roles, name="Muted")
                )
                await redis.delete(key)

    @auto_unmute.before_loop
    async def before_auto_unmute(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="unmute", description="Unmute a user from the server.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(member="The member to unmute.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if discord.utils.get(interaction.guild.roles, name="Muted") is None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Something went wrong!",
                    description="The user isn't muted!",
                    color=color.gold(),
                )
            )
            return
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
        await redis.delete(f"mute_{interaction.guild.id}-{member.id}")

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Done!",
                description=f"Successfully unmuted {member.mention}.",
                color=color.gold(),
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot), guilds=[discord.Object(id=883413709031108608)])
