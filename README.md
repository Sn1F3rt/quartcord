# quartcord

[![PyPI](https://img.shields.io/pypi/v/quartcord)](https://pypi.org/project/quartcord/) [![Read the Docs](https://img.shields.io/readthedocs/quartcord)](https://quartcord.readthedocs.io/en/latest/) 

## Table of Contents

- [About](#about)
- [Installation](#installation)
  * [Requirements](#requirements)
  * [Setup](#setup)
- [Basic Example](#basic-example)
- [Documentation](#documentation)
- [Support](#support)
- [Credits](#credits)
- [License](#license)

## About

Discord OAuth2 extension for Quart.

## Installation

### Requirements

- Quart
- pyjwt
- aiohttp
- oauthlib
- discord.py
- cachetools
- Async-OAuthlib

### Setup

To install current latest release you can use following command:
```sh
python -m pip install quartcord
```

## Basic Example

```python
from quart import Quart, redirect, url_for
from quartcord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Quart(__name__)

app.secret_key = b"random bytes representing quart secret key"

app.config["DISCORD_CLIENT_ID"] = 490732332240863233  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = ""  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = ""  # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = ""  # Required to access BOT resources.

discord = DiscordOAuth2Session(app)


@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
async def me():
    user = await discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()
```

## Documentation

Head over to [documentation](https://quartcord.readthedocs.io/en/latest/) for full API reference. 

## Support

- [Project Issues](https://github.com/Sn1F3rt/quartcord/issues)
- [FumeStop Community Server](https://fumes.top/community) **(``Help > quartcord``)**

## Credits

- [Flask-Discord](https://github.com/weibeu/Flask-Discord/)
- [Quart-Discord](https://github.com/jnawk/Quart-Discord/) **(Do not use; no longer maintained)**

## License

[MIT License](LICENSE)

Copyright &copy; 2023 Sayan "Sn1F3rt" Bhattacharyya
