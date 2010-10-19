from scriptutils.arguments import Arguments

from .cli import main as main_cli
from .gui import main as main_gui

from . import WALLPAPER_COMMANDS

def get_arguments(): #{{{1
    a = Arguments(description="Tool for managing desktop backgrounds.")
    a.add_argument('-v', '--verbose', default=False, action='store_true', help='be verbose')
    a.add_argument('-t', '--target', default=None, type='int', help='restrict to specific monitor')
    a.add_argument('-c', '--command', default=None, type='choice', choices=WALLPAPER_COMMANDS, help='command to change wallpaper')
    a.add_argument('-r', '--refresh', default=False, action='store_true', help='refresh the display')
    a.add_argument('-s', '--search', metavar='REGEX', action='append', help='search filenames based on REGEX')
    a.add_argument('-x', '--exclude', metavar='REGEX', action='append', help='exclude filenames based on REGEX')
    a.add_argument('-g', '--gui', default=False, action='store_true', help='use gui mode')
    return a.parse_args()

def main(): #{{{1
    args = get_arguments()
    m = main_gui if args.gui else main_cli
    m(args)
