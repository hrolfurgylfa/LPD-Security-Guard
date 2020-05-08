# Community
from discord.ext import commands

class LPDOnly(commands.CheckFailure):
    """Exception raised when an LPD only command is used by a non-lpd member.
    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message=None):
        super().__init__(message or 'This command can only be used by LPD members.')

class WhiteShirtOnly(commands.CheckFailure):
    """Exception raised when an LPD only command is used by a non-lpd member.
    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message=None):
        super().__init__(message or 'This command can only be used by LPD White Shirts.')

class WrongChannel(commands.CheckFailure):
    """Exception raised when a command is used in a channel it cannot be used in.
    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message=None):
        super().__init__(message or 'This command cannot be used in this channel.')

class WrongServer(commands.CheckFailure):
    """Exception raised when a command is used in a server that is not supported.
    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message=None):
        super().__init__(message or 'This bot does not work in this server.')
