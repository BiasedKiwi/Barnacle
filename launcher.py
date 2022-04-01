#!/usr/bin/env python
from barnacle import Barnacle
import os
import sys
from dotenv import load_dotenv
import logging
from datetime import datetime


now = datetime.now()

logger = logging.getLogger("discord")  # Set up logging
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f"./logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

instance = Barnacle()  # Initialise a Barnacle instance


load_dotenv()  # Load the .env file
if len(sys.argv) > 1:   # Set the token
    token = sys.argv[1]
    instance.set_token(token)
else:  # If the token was not specified via the command line arguments, attempt to fetch it from the environment
    token = os.environ.get("BARNACLE_TOKEN")
    if token is None:
        print("Please provide a valid Discord API token. (Example: 'python3 launcher.py <token> <prefix>')")
        print("You can also set an environment variable 'BARNACLE_TOKEN' for access to the token by barnacle.")
        exit(1)
    instance.set_token(token)  # Set the token from an environment variable

if len(sys.argv) > 2:   # Set the prefix
    token = sys.argv[2]
    instance.set_prefix(token)
else:  # If the prefix was not specified via the command line arguments, attempt to fetch it from the environment
    token = os.environ.get("BARNACLE_PREFIX")
    if token is None:
        print("Please provide a valid Barnacle prefix. (Example: 'python3 launcher.py <token> <prefix>')")
        print("You can also set an environment variable 'BARNACLE_PREFIX' for access to the token by barnacle.")
        exit(1)
    instance.set_prefix(token)  # Set the prefix from an environment variable
    
strip_after_prefix = os.getenv("BARNACLE_STRIP")
case_insensitive = os.getenv("BARNACLE_CASE")

if strip_after_prefix is None or case_insensitive is None:
    print("Warning: BARNACLE_STRIP and BARNACLE_CASE environment variables were not set. Defaulting to True for both.")

instance.start()  # Start the Barnacle instance
