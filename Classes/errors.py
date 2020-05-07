# Community
from discord.ext import commands

class WrongChannelForCommand(commands.CheckFailure):
    """Exception raised when a command is used in the wrong channel.
    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message=None):
        super().__init__(message or 'This command does not work in this channel.')

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