Wally is a tool for managing desktop wallpapers.

Wally was created because desktop environments in Linux lack the ability to
set wallpapers on a per-monitor basis. This is mainly due to the fact that
multi-display setups in X are seen as a single screen. For example, two
1600x1200 monitors would actually be a 3200x1200 screen in a side-by-side
configuration. Currently, Wally only supports Gnome. I would like to add
support for KDE, but I have no need for it right now.

The only assumptions that Wally makes about your collection of wallpapers is
that they are organized into a central folder for each type of display. The
following display types are supported:

    netbook
    standard
    widescreen

All configuration can be done through the gui version (wally-gui), but I will
describe the manual configuration, as well.

The configuration file will be created on the first invocation, and will be
located at:

    ~/.wally/main.cfg

You'll want to specify where to look for wallpapers. This is done by
specifying a list of directories for each display type. (multiple directories
are comma-separated):

For example, in the [directories] section of the configuration file, you might
have the following specified:

    standard = /usr/share/backgrounds, ~/wallpapers/standard

For each monitor that you have, the display type will be automatically
determined and a wallpaper from the appropriate directory will be chosen.

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

Examples of Usage
-----------------

See the current status:

    wally -v

Choose a wallpaper at random from all sources:

    wally -c random

Choose the next wallpaper for display 0 (primary):

    wally -t0 -c next

Choose a random wallpaper matching the regular expression "narwhal":

    wally -c random -s "narwhal"

Installation
------------

If you have setuptools installed, you can install Wally with:

    pip install Wally

Or:

    easy_install Wally

Otherwise, you'll have to download the package and run:

    python setup.py install

If you install it this way then you will also have to install all necessary
dependencies manually.

Scheduling Wallpaper Changes
----------------------------

One of the first things you may want to do is schedule Wally to change the
wallpaper periodically. I recommend using gnome-schedule, as it's easiest to
setup. Simply put the following in the command field:

    /path/to/wally -c random

Change the behavior to "X application". This will ensure that the scheduler is
aware of the display that will be updated.

Set your desired frequency of execution and you're done.
