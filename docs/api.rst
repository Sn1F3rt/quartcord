API Reference
=============

This sections has reference to all of the available classes, their
attributes and available methods.


Discord OAuth2 Client
---------------------

.. autoclass:: quartcord.DiscordOAuth2Session
    :members:
    :inherited-members:

.. autoclass:: quartcord._http.DiscordOAuth2HttpClient
    :members:
    :inherited-members:


Models
------

.. autoclass:: quartcord.models.Guild
    :members:
    :inherited-members:

.. autoclass:: quartcord.models.User
    :members:
    :inherited-members:

.. autoclass:: quartcord.models.Bot
    :members:
    :inherited-members:

.. autoclass:: quartcord.models.Integration
    :members:
    :inherited-members:

.. autoclass:: quartcord.models.UserConnection
    :members:
    :inherited-members:


Utilities
---------

.. autodecorator:: quartcord.requires_authorization


Exceptions
----------

.. autoclass:: quartcord.HttpException
    :members:

.. autoclass:: quartcord.RateLimited
    :members:

.. autoclass:: quartcord.Unauthorized
    :members:

.. autoclass:: quartcord.AccessDenied
    :members:
