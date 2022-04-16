# Barnacle

## Hosting locally

To host Barnacle locally, you'll first have to follow a few steps to set up Barnacle.

1. Clone the repository using [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

```shell
$ git clone https://github.com/shadawcraw/Barnacle.git

$ cd Barnacle  # Move into the repository's directory
```

2. Once you've cloned the repository, you'll need to install the dependencies using `pip`.

```shell
$ pip3 install -r requirements.txt  # Linux/WSL/MacOS
$ py -m pip install -r requirements.txt  # Windows
```

3. Once you've installed the dependencies, you will need to set up the token that will be used to run the bot.
    
    1. Go to https://discord.com/developers/applications

    2. Click on the "New Application" button. Enter a name, and proceed.

    3. While on the page of our newly created app, navigate to the "Bot" tab.

    4. Click on the "Add a Bot" button.

    5. IMPORTANT: If you are planning to use message commands, scroll down to the Privileged Gateway Intents section and toggle the "Message Content Intent"

    6. On the "Bot" tab, click on the "Reset Token" button, follow the prompts, and carefully save the token.

5. Back in the project's root directory, create a file named ".env"

6. In the file, enter the following: "BARNACLE_TOKEN=<token>" where <token> is the token you just generated.

7. In the same file, add a the following: "BARNACLE_PREFIX=<prefix>" where <prefix> is the prefix you want to use for your commands.

8. You're done! All you need to do now is run `launcher.py` in the root directory.

```shell
$ python3 launcher.py  # Linux/WSL/MacOS

$ py launcher.py  # Windows
```
    
## License
    
Barnacle is licensed under the GNU General Public License v3.0. See [LICENSE](https://github.com/shadawcraw/Barnacle/blob/main/LICENSE) for details.
