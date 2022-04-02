#!/usr/bin/env python
import os

import discord
from discord.ext import commands


class Barnacle:
    def __init__(self, token="", prefix=".", case_insensitive=True, strip_after_prefix=True):
        self.token = token
        self.prefix = prefix
        self.case_insensitive = case_insensitive
        self.strip_after_prefix = strip_after_prefix
        self.client = commands.AutoShardedBot(  # Initialise the bot instance
            command_prefix=self.prefix,
            case_insensitive=self.case_insensitive,
            strip_after_prefix=self.strip_after_prefix,
            help_command=None
        )

    def set_token(self, token):
        self.token = token
        
    def get_token(self):
        print(self.token)

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_case_insensitive(self, case_insensitive):
        self.case_insensitive = case_insensitive

    def set_strip_after_prefix(self, strip_after_prefix):
        self.strip_after_prefix = strip_after_prefix
        
    def load_cogs(self, directory: str):
        """Load all cogs in a given directory in O(n) time."""
        os.chdir(directory)
        for _, _, f_name in os.walk(os.getcwd()):  # Iterate through all the files in a directory
            for item in f_name:
                if item.endswith(".py"):
                    self.client.load_extension(f"barnacle.extensions.{item[:-3]}")  # TODO: Find a way to determine "barnacle.extensions." without hardcoding the value.

    def start(self):
        # Set the events
        @self.client.event
        async def on_ready():
            print("Barnacle is online and connected to Discord.")
            
        os.chdir("./barnacle")
        self.load_cogs("./extensions")
            
        try:
            self.client.run(self.token)
        except discord.errors.LoginFailure:
            print("An invalid token was passed.")
            exit(1)
        except discord.errors.GatewayNotFound:
            print("An error occured. This might happen when Discord is down. Please try again later.")
            exit(1)


if __name__ == "__main__":
    print("Please launch the launcher.py file instead of this one directly.")
    exit(1)
