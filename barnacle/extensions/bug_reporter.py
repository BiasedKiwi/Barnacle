import json
import os

import discord
import requests
from barnacle import PrettyPrinter, config
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class BugReportForm(discord.ui.Modal, title="Bug Reporter"):
    command_concerned = discord.ui.TextInput(
        label="What command is concerned by this bug?"
    )
    summary = discord.ui.TextInput(
        label="Please give a short summary of the bug", style=discord.TextStyle.long
    )
    expected_behavior = discord.ui.TextInput(
        label="What was supposed to happen?", style=discord.TextStyle.long
    )
    actual_behavior = discord.ui.TextInput(
        label="What actually happened?", style=discord.TextStyle.long
    )
    steps_to_reproduce = discord.ui.TextInput(
        label="How can we reproduce this bug?", style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        issue = {
            "title": f"[Automatic Bug Report] {self.summary.value}",
            "body": f"## What command is concerned?\n{self.command_concerned.value}\n\n## What was supposed to happen?\n{self.expected_behavior.value}\n\n## What actually happened?\n{self.actual_behavior.value}\n\n## How can we reproduce this bug?\n{self.steps_to_reproduce.value}\n\n This issue has been reported by {interaction.user}",
            "labels": ["bug"],
        }
        repo = config.detect_config("../config")[1][0]["bot_info"][2]["repo_short"]
        url = f"https://api.github.com/repos/{repo}/issues"  # If you are self-hosting, change the value in `settings.yaml`
        with requests.Session() as session: # If you are self-hosting, change this to your own credentials
            session.auth = ("shadawcraw", os.environ.get("BARNACLE_GH_TOKEN"))
            r = session.post(url, json.dumps(issue))
        if r.status_code == 201:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Thank you!",
                    description="Thank you for reporting this bug! Our team will take a look at it shortly.",
                    color=discord.Color.gold(),
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="An error occurred!",
                    description="Please try again.",
                    color=discord.Color.gold(),
                ).add_field(name="Debug Info", value="Response code: " + str(r.status_code)),
                ephemeral=True
            )


class BugReporter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.pretty_print = PrettyPrinter()
        print("Bug Reporter cog is ", end="")
        self.pretty_print.green("online")

    @app_commands.command(name="bug", description="Report a bug.")
    async def bug_report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugReportForm())


async def setup(bot: commands.Bot):
    await bot.add_cog(BugReporter(bot), guilds=[discord.Object(id=883413709031108608)])
