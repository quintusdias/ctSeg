# This allows both python2 and python3 to run the same code.
import sip
sip.setapi('QString', 2)

from . import command_line

__all__ = [command_line]
