# Description {{{1

"""Tool for managing desktop wallpapers.

Wally was created because desktop environments in Linux lack the ability to
set wallpapers on a per-monitor basis. This is mainly due to the fact that
multi-display setups in X are seen as a single screen. For example, two
1600x1200 monitors would actually be a 3200x1200 screen in a side-by-side
configuration. Currently, Wally only supports Gnome. I would like to add
support for KDE, but I have no need for it right now.

The only assumptions that Wally makes about your collection of wallpapers is
that they are organized into a central folder for each type of operation. The
only operation that most people want is 'scale', which resizes the wallpaper
while keeping the same aspect ratio. The following resizing operations are
supported:

    scale
    multi
    tile
    zoom
    center
    stretch

The configuration file will be created on the first invocation, and will be
located at:

    ~/.wally/main.cfg

You'll want to specify where to look for wallpapers. This is done with one or
more of the following options (multiple directories are comma-separated):

    scale
    multi
    tile
    zoom
    center
    stretch

Example:

    scale = /usr/share/backgrounds, ~/wallpapers/scale
    multi = ~/wallpapers/multi

You may not want all of your wallpapers to be considered when choosing a new
one. You can set this with the 'exclusions' option (values are regular
expressions and are comma-separated):

Example:

    exclusions = .*\.png, /some/folder/to/exlude, partial/path, /nsfw/

In the instances where the image does not cover the entire monitor, the color
black will be used as the wallpaper. You can change this with the
'background_color' option (specified as a hex triplet):

Example:

    background_color = #000000

Wally can be invoked directly at the command line, but it is often easier to
create launchers to execute common commands. To see available options, run the
following command at the command line:

    wally --help

Some examples of typical usage:

    See the current status:
        wally -v

    Choose a wallpaper at random from all sources:
        wally -c random

    Choose the next wallpaper for display 0 (primary):
        wally -t0 -c next

    Random wallpaper for display 1 that matches the pattern 'fractal' or
    'family photos':
        wally -t1 -c random fractal "family photos"

    Random wallpaper that matches 'family photos', but without 'Jeremy':
        wally -c rantom 'family photos' - 'jeremy'

""" #}}}

__appname__ = 'Wally'
__author__  = 'Jeremy Cantrell <jmcantrell@gmail.com>'
__url__     = 'http://jmcantrell.me'
__date__    = 'Tue 2008-02-05 14:55:05 (-0500)'
__license__ = 'GPL'

from .utils import uniqify

ASPECT_RATIOS = {
        (128, 75): 'netbook',
        (4, 3): 'standard',
        (8, 5): 'widescreen',
        }

WALLPAPER_TYPES = uniqify(ASPECT_RATIOS.values())

WALLPAPER_COMMANDS = ['random', 'next', 'prev']
