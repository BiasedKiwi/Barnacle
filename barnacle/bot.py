#!/usr/bin/env python
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
            strip_after_prefix=self.strip_after_prefix
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

    def start(self):
        # Set the events
        
        @self.client.event
        async def on_ready():
            print("Barnacle is online and connected to Discord.")
            
        try:
            self.client.run(self.token)
        except discord.errors.LoginFailure:
            print("An invalid token was passed.")
            exit(1)
        except discord.errors.GatewayNotFound:
            print("The gateway hub for the Client websocket could not be found. This might happen when Discord is down. Please try again later.")
            exit(1)


if __name__ == "__main__":
    print("Please launch the launcher.py file instead of this one directly.")
    exit(1)
