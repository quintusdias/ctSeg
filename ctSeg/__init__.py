import sip

from . import command_line

# This allows both python2 and python3 to run the same code.
sip.setapi('QString', 2)

__all__ = [command_line]
