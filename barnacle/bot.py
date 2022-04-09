#!/usr/bin/env python
import os
from typing import List, Union

import discord
from discord.ext import commands
from .rich_printer import PrettyPrinter


class Barnacle:
    def __init__(self, token="", prefix=".", case_insensitive=True, strip_after_prefix=True):
        self.token = token
        self.prefix = prefix
        self.case_insensitive = case_insensitive
        self.strip_after_prefix = strip_after_prefix
        self.pretty_printer = PrettyPrinter()
        self.client = commands.AutoShardedBot(  # Initialise the bot instance
            command_prefix=self.prefix,
            case_insensitive=self.case_insensitive,
            strip_after_prefix=self.strip_after_prefix,
            help_command=None
        )

    def set_token(self, token: str) -> None:
        """Set the token that will be used to connect to the Discord API."""
        self.token = token
        
    def get_token(self) -> str:
        """Fetch the token to be used to connect to the Discord API. Stored in `self.token`"""
        return self.token

    def set_prefix(self, prefix: Union[List, str]) -> None:
        """Set the prefix to be used with the bot."""
        self.prefix = prefix
        
    def get_prefix(self) -> List:
        """Fetch a list of the prefixes to be used with the bot"""
        return self.prefix

    def set_case_insensitive(self, case_insensitive: bool) -> None:
        """Set the case insensitive flag to be used with the bot."""
        self.case_insensitive = case_insensitive

    def set_strip_after_prefix(self, strip_after_prefix: bool) -> None:
        """Set the strip after prefix flag to be used with the bot."""
        self.strip_after_prefix = strip_after_prefix
        
    def load_cogs(self, directory: str, subdir: str = "") -> None:
        """Load all cogs in a given directory in a recursive fashion."""
        os.chdir(directory)
        base = os.getcwd()
        for file in os.listdir():  # Iterate through all the files in a directory
            if file.endswith(".py"):
                if subdir != "":
                    self.client.load_extension(f"barnacle.extensions.{subdir}.{file[:-3]}")  # TODO: Find a way to determine "barnacle.extensions." without hardcoding the value.
                else:
                    self.client.load_extension(f"barnacle.extensions.{file[:-3]}")
            elif os.path.isdir(os.path.join(base, file)):
                os.chdir(os.path.join(base, file))
                self.load_cogs(os.getcwd(), subdir = file)
                os.chdir(base)

    def start(self) -> None:
        """Start the bot using `client.run`."""
        # Set the events
        @self.client.event
        async def on_ready():
            self.pretty_printer.bold("Barnacle is online and connected to Discord.")
            
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
