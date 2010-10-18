from argparse import ArgumentParser

from .cli import main as main_cli
from .gui import main as main_gui

from . import WALLPAPER_COMMANDS

def get_options(): #{{{1
    opts = ArgumentParser(description="Tool for managing desktop backgrounds.")
    opts.add_argument('-v', '--verbose', default=False, action='store_true', help='be verbose')
    opts.add_argument('-t', '--target', default=None, type='int', help='restrict to specific monitor')
    opts.add_argument('-c', '--command', default=None, type='choice', choices=WALLPAPER_COMMANDS, help='command to change wallpaper')
    opts.add_argument('-r', '--refresh', default=False, action='store_true', help='refresh the display')
    opts.add_argument('-s', '--search', metavar='REGEX', action='append', help='search filenames based on REGEX')
    opts.add_argument('-x', '--exclude', metavar='REGEX', action='append', help='exclude filenames based on REGEX')
    opts.add_argument('-g', '--gui', default=False, action='store_true', help='use gui mode')
    return opts.parse_args()

def main(): #{{{1
    opts = get_options()
    m = main_gui if opts.gui else main_cli
    m(opts)
