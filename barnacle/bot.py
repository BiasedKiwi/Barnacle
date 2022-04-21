#!/usr/bin/env python
import os
import sys

from discord.ext import commands

from .rich_printer import PrettyPrinter


class Barnacle(commands.AutoShardedBot):
    def __init__(
        self, **kwargs
    ):
        self.prefix = kwargs["command_prefix"]
        self.case_insensitive = True
        self.strip_after_prefix = True
        self.pretty_printer = PrettyPrinter()
        super().__init__(**kwargs)
        
    async def setup_hook(self):
        await self.load_cogs(client=self, directory="./barnacle/extensions")

    async def load_cogs(self, client, directory: str, subdir: str = "") -> None:
        """Load all cogs in a given directory in a recursive fashion."""
        os.chdir(directory)
        base = os.getcwd()
        for file in os.listdir():  # Iterate through all the files in a directory
            if file.endswith(".py"):
                if subdir != "":
                    await client.load_extension(
                        f"barnacle.extensions.{subdir}.{file[:-3]}"
                    )  # As of Discord.py 2.0, `load_extension` is a coroutine.
                else:
                    await client.load_extension(
                        f"barnacle.extensions.{file[:-3]}"
                    )  # Refer to comment on line 61.
            elif os.path.isdir(os.path.join(base, file)):
                os.chdir(os.path.join(base, file))
                await self.load_cogs(client, os.getcwd(), subdir=file)  # Recursive call
                os.chdir(base)


if __name__ == "__main__":
    print("Please launch the launcher.py file instead of this one directly.")
    sys.exit(1)
