#!/usr/bin/env python

# Description {{{1
"""Tool for managing desktop backgrounds.

Wally was created because desktop environments in Linux lack the ability to
set backgrounds on a per-monitor basis. This is mainly due to the fact that
multi-display setups in X are seen as a single screen. For example, two
1600x1200 monitors would actually be a 3200x1200 screen in a side-by-side
configuration. Currently, Wally only supports Gnome. I would like to add
support for KDE, but I have no need for it right now.

The only assumptions that Wally makes about your collection of backgrounds is
that they are organized into a central folder for each type of operation. The
only operation that most people want is 'scale', which resizes the background
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

    ~/.wally/config

You'll want to specify where to look for backgrounds. This is done with one or
more of the following options (multiple directories are comma-separated):

    directories_scale
    directories_multi
    directories_tile
    directories_zoom
    directories_center
    directories_stretch

Example:

    directories_scale = /usr/share/backgrounds, ~/backgrounds/scale
    directories_multi = ~/backgrounds/multi

You may not want all of your backgrounds to be considered when choosing a new
one. You can set this with the following option (values are regular expressions
and are comma-separated):

    exclusion_patterns

Example:

    exclusion_patterns = .*\.png, /some/folder/to/exlude, partial/path, /nsfw/

In the instances where the image does not cover the entire monitor, the color
black will be used as the background. You can change this with the following
option (specified as a three color RGB value):

    background_color

Example:

    background_color = 139, 0, 139

Wally can be invoked directly at the command line, but it is often easier to
create launchers to execute common commands. To see available options, run the
following command at the command line:

    wally --help

Some examples of typical usage:

    See the current status:

        wally -v

    Choose a background at random from all sources:

        wally -c random

    Choose the next background for display 0 (primary):

        wally -t0 -c next

    Choose a random background for display 1 that matches the pattern 'fractal'
    or 'family photos':

        wally -t1 -c random fractal "family photos"

    Choose a random background that matches 'family photos', but without
    'Jeremy':

        wally -c rantom 'family photos' - 'jeremy'
""" #}}}

__appname__ = 'Wally'
__authors__ = ['Jeremy Cantrell <jmcantrell@gmail.com>']
__url__     = 'http://jeremycantrell.com'
__date__    = 'Tue 2008-02-05 14:55:05 (-0500)'
__license__ = 'GPL'

WALLPAPER_TYPES = ['scale', 'multi', 'tile', 'stretch', 'zoom', 'center']

from .main import Wally
from .gui import main as main_gui
from .console import main as main_console
