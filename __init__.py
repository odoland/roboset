"""A robot to play the card game Set
"""

__author__ = 'odoland'
__date__ = '2018-10-14'
NAME = 'Orlando'

import sys
assert sys.version_info >= (3, 6), "Your version of python is too old to use f strings."

from pathlib import Path
IMGDIR = Path(__file__).parent / Path('img/')

from .SetCard import DIAMOND, SQUIGGLE, OVAL
from .SetCard import PURPLE, GREEN, RED
from .SetCard import HOLLOW, STRIPE, FULL
from .SetCard import ONE, TWO, THREE
