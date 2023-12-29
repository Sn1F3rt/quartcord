.. _intro:



Introduction
============

``quartcord`` is an extension for Quart - Python web framework which
makes easy implementation of Discord OAuth2 API. After creating a discord
client object, one can easily request authorization and hence any of the
resources provided by the discord OAuth2 API under the available scope
permissions.

Requirements
------------

- Quart
- pyjwt
- aiohttp
- oauthlib
- discord.py
- cachetools
- Async-OAuthlib

Installing
----------

You can install ``quartcord`` directly from PyPI using PIP and following command
in shell or command prompt: ::

    python -m pip install -U quartcord

You can also install the latest development version (**maybe unstable/broken**) by
using following command: ::

    python -m pip install -U git+https://github.com/Sn1F3rt/quartcord.git


Basic Usage
-----------
Here is a simple example to get users authorization token using OAuth2 and use it
in exchange for fetching user's details and display them on web page.


.. code-block:: python3

    from quart import Quart, redirect, url_for
    from quartcord import DiscordOAuth2Session, requires_authorization, Unauthorized

    app = Quart(__name__)

    app.secret_key = b"random bytes representing quart secret key"

    app.config["DISCORD_CLIENT_ID"] = 490732332240863233    # Discord client ID.
    app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
    app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
    app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.


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
