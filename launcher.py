#!/usr/bin/env python
"""Launcher script for Barnacle."""


import logging
import os
import sys
from datetime import datetime
import discord
from dotenv import load_dotenv

from barnacle import Barnacle

now = datetime.now()

logger = logging.getLogger("discord")  # Set up logging
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename=f"./logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log",
    encoding="utf-8",
    mode="w",
)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# Constants
TOKEN = ""
PREFIX = ""


load_dotenv()  # Load the .env file
if len(sys.argv) > 1:  # Check if the token was passed in the command line arguments
    token = sys.argv[1]
else:  # If the token was not specified via the command line arguments, attempt to fetch it from the environment
    token = os.environ.get(
        "BARNACLE_TOKEN"
    )  # Fetch the token from the .env file which should be placed in the root of the project.
    if token is None:  # If the token was not found in the .env file, exit the program
        print(
            "Please provide a valid Discord API token. (Example: 'python3 launcher.py <token> <prefix>')"
        )
        print(
            "You can also set an environment variable 'BARNACLE_TOKEN' for access to the token by barnacle."
        )
        sys.exit(1)
TOKEN = token

if len(sys.argv) > 2:  # Check if the prefix was passed in the command line arguments
    prefix = sys.argv[2]
else:  # If the prefix was not specified via the command line arguments, attempt to fetch it from the environment
    prefix = os.environ.get("BARNACLE_PREFIX")
    if prefix is None:
        print(
            "Please provide a valid Barnacle prefix. (Example: 'python3 launcher.py <token> <prefix>')"
        )
        print(
            "You can also set an environment variable 'BARNACLE_PREFIX' for access to the token by barnacle."
        )
        sys.exit(1)
PREFIX = prefix


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
instance = Barnacle(
    command_prefix=PREFIX,
    intents=intents,
    strip_after_prefix=True,
    case_insensitive=True,
)  # Initialise a Barnacle instance


instance.run(TOKEN)
