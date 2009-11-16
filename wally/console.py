from scriptutils.options import Options
from .main import Wally
from . import WALLPAPER_COMMANDS

def get_options(): #{{{1
    opts = Options()
    opts.add_option('-v', '--verbose', default=False, action='store_true', help='Be verbose.')
    opts.add_option('-t', '--target', default=None, type='int', help='Restrict to specific monitor.')
    opts.add_option('-c', '--command', default=None, type='choice', choices=WALLPAPER_COMMANDS, help='Command to change wallpaper.')
    opts.add_option('-r', '--refresh', default=False, action='store_true', help='Refresh the display.')
    opts.add_option('-s', '--search', metavar='REGEX', action='append', help='Search filenames based on REGEX.')
    opts.add_option('-x', '--exclude', metavar='REGEX', action='append', help='Exclude filenames based on REGEX.')
    return opts.parse_args()

def main(): #{{{1
    opts, args = get_options()
    w = Wally()
    if opts.search: w.searches = opts.search
    if opts.exclude: w.exclusions = opts.exclude
    w.refresh_wallpapers()
    if opts.command: getattr(w, 'change_%s' % opts.command)(opts.target)
    if opts.verbose: print '\n'.join(w.display)
    if opts.command or opts.refresh: w.refresh_display()
