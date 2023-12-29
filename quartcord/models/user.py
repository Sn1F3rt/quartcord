import math

from .. import configs

from .guild import Guild
from .. import exceptions
from .base import DiscordModelsBase
from .connections import UserConnection

from quart import current_app, session


class User(DiscordModelsBase):
    """Class representing Discord User.


    Operations
    ----------
    x == y
        Checks if two user's are the same.
    x != y
        Checks if two user's are not the same.
    str(x)
        Returns the user's name with discriminator.

    Attributes
    ----------
    id : int
        The discord ID of the user.
    username : str
        The discord username of the user.
    display_name: str
        The global display name of the user.
    discriminator : str
        A four length string representing discord tag of the user (deprecated).
    avatar_hash : str
        Hash of users avatar.
    bot : bool
        A boolean representing whether the user belongs to an OAuth2 application.
    mfa_enabled : bool
        A boolean representing whether the user has two factor enabled on their account.
    locale : str
        The user's chosen language option.
    verified : bool
        A boolean representing whether the email on this account has been verified.
    email : str
        User's email ID.
    flags : int
        An integer representing the
        `user flags <https://discordapp.com/developers/docs/resources/user#user-object-user-flags>`_.
    premium_type : int
        An integer representing the
        `type of nitro subscription <https://discordapp.com/developers/docs/resources/user#user-object-premium-types>`_.
    connections : list
        A list of :py:class:`quartcord.UserConnection` instances. These are cached and this list might be empty.

    """

    ROUTE = "/users/@me"

    def __init__(self, payload):
        super().__init__(payload)
        self.id = int(self._payload["id"])
        self.username = self._payload["username"]
        self.display_name = self._payload["global_name"]
        self.discriminator = self._payload["discriminator"]
        self.avatar_hash = self._payload.get("avatar", self.discriminator)
        self.bot = self._payload.get("bot", False)
        self.mfa_enabled = self._payload.get("mfa_enabled")
        self.locale = self._payload.get("locale")
        self.verified = self._payload.get("verified")
        self.email = self._payload.get("email")
        self.flags = self._payload.get("flags")
        self.premium_type = self._payload.get("premium_type")

        # Few properties which are intended to be cached.
        self._guilds = None  # Mapping of guild ID to quartcord.models.Guild(...).
        self.connections = None  # List of quartcord.models.UserConnection(...).

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, user):
        return isinstance(user, User) and user.id == self.id

    def __ne__(self, user):
        return not self.__eq__(user)

    @staticmethod
    def check_size(size: int):
        if (
            not isinstance(size, int)
            or not size in range(16, 4097)
            or not math.log2(size).is_integer()
        ):
            raise ValueError("Size must be a power of two between 16 and 4096.")

    @property
    def name(self):
        """An alias to the username attribute."""
        return self.username

    @property
    def avatar_url(self, size: int = 1024):
        """A property returning direct URL to user's avatar.

        Parameters
        ----------
        size : int
            The resolution of the avatar. Can be any power of two between 16 and 4096. Defaults to 1024.

        Returns
        -------
        str
            The Discord CDN URL to user's avatar.
        None
            If user doesn't have any avatar set.

        """
        if not self.avatar_hash:
            return

        self.check_size(size)

        image_format = (
            configs.DISCORD_ANIMATED_IMAGE_FORMAT
            if self.is_avatar_animated
            else configs.DISCORD_IMAGE_FORMAT
        )

        return configs.DISCORD_USER_AVATAR_BASE_URL.format(
            user_id=self.id,
            avatar_hash=self.avatar_hash,
            format=image_format,
            size=size,
        )

    @property
    def default_avatar_url(self, size: int = 1024):
        """A property which returns the default avatar URL as when user doesn't have any avatar set.

        Parameters
        ----------
        size : int
            The resolution of the avatar. Can be any power of two between 16 and 4096. Defaults to 1024.

        Returns
        -------
        str
            The Discord CDN URL to user's avatar.
        None
            If user doesn't have any avatar set.

        """

        self.check_size(size)

        if int(self.discriminator):
            index = int(self.discriminator) % 5

        else:
            index = (self.id >> 22) % 6

        return configs.DISCORD_DEFAULT_USER_AVATAR_BASE_URL.format(
            index=index, size=size
        )

    @property
    def is_avatar_animated(self):
        """A boolean representing if avatar of user is animated. Meaning user has GIF avatar."""
        try:
            return self.avatar_hash.startswith("a_")
        except AttributeError:
            return False

    @property
    def guilds(self):
        """A cached mapping of user's guild ID to :py:class:`quartcord.Guild`. The guilds are cached when the first
        API call for guilds is requested, so it might be an empty dict.
        """
        try:
            return list(self._guilds.values())
        except AttributeError:
            pass

    @guilds.setter
    def guilds(self, value):
        self._guilds = value

    @classmethod
    async def fetch_from_api(cls, guilds=False, connections=False):
        """A class method which returns an instance of this model by implicitly making an
        API call to Discord. The user returned from API will always be cached and update in internal cache.

        Parameters
        ----------
        guilds : bool
            A boolean indicating if user's guilds should be cached or not. Defaults to ``False``. If chose to not
            cache, user's guilds can always be obtained from :py:func:`quartcord.Guilds.fetch_from_api()`.
        connections : bool
            A boolean indicating if user's connections should be cached or not. Defaults to ``False``. If chose to not
            cache, user's connections can always be obtained from :py:func:`quartcord.Connections.fetch_from_api()`.

        Returns
        -------
        cls
            An instance of this model itself.
        [cls, ...]
            List of instances of this model when many of these models exist.

        """
        self = await super().fetch_from_api()
        current_app.discord.users_cache.update({self.id: self})
        session["DISCORD_USER_ID"] = self.id

        if guilds:
            await self.fetch_guilds()
        if connections:
            await self.fetch_connections()

        return self

    @classmethod
    def get_from_cache(cls):
        """A class method which returns an instance of this model if it exists in internal cache.

        Returns
        -------
        quartcord.User
            An user instance if it exists in internal cache.
        None
            If the current doesn't exists in internal cache.

        """
        return current_app.discord.users_cache.get(current_app.discord.user_id)

    async def add_to_guild(self, guild_id) -> dict:
        """Method to add user to the guild, provided OAuth2 session has already been created with ``guilds.join`` scope.

        Parameters
        ----------
        guild_id : int
            The ID of the guild you want this user to be added.

        Returns
        -------
        dict
            A dict of guild member object. Returns an empty dict if user is already present in the guild.

        Raises
        ------
        quartcord.Unauthorized
            Raises :py:class:`quartcord.Unauthorized` if current user is not authorized.

        """
        try:
            data = {
                "access_token": (await current_app.discord.get_authorization_token())[
                    "access_token"
                ]
            }
        except KeyError:
            raise exceptions.Unauthorized
        return (
            await self._bot_request(
                f"/guilds/{guild_id}/members/{self.id}", method="PUT", json=data
            )
            or dict()
        )

    async def get_guilds(self) -> list:
        """A method returns the user's guilds from cache or makes an API call to Discord to get user's guilds.

        Returns
        -------
        list
            List of :py:class:`quartcord.Guilds` instances.

        """
        return self.guilds or await self.fetch_guilds()

    async def fetch_guilds(self) -> list:
        """A method which makes an API call to Discord to get user's guilds. It prepares the internal guilds cache
        and returns list of all guilds the user is member of.

        Returns
        -------
        list
            List of :py:class:`quartcord.Guilds` instances.

        """
        self._guilds = {
            guild.id: guild for guild in await Guild.fetch_from_api(cache=False)
        }
        return self.guilds

    async def fetch_connections(self) -> list:
        """A method which makes an API call to Discord to get user's connections. It prepares the internal connection
        cache and returns list of all connection instances.

        Returns
        -------
        list
            A list of :py:class:`quartcord.UserConnection` instances.

        """
        self.connections = await UserConnection.fetch_from_api(cache=False)
        return self.connections
