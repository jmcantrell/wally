__appname__ = 'Wally'
__author__  = 'Jeremy Cantrell <jmcantrell@gmail.com>'
__url__     = 'http://jmcantrell.me'
__date__    = 'Sun 2010-02-14 22:16:44 (-0500)'
__license__ = 'GPL'

from .utils import uniqify

ASPECT_RATIOS = {
        (128, 75): 'netbook',
        (4, 3): 'standard',
        (8, 5): 'widescreen',
        }

WALLPAPER_TYPES = uniqify(ASPECT_RATIOS.values())

WALLPAPER_COMMANDS = ['random', 'next', 'prev']
