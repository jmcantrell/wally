from scriptutils.options import Options
from .main import Wally
from . import WALLPAPER_COMMANDS

def get_options(): #{{{1
    opts = Options('Usage: %prog [options]', width=35)
    opts.add_option('-h', '--help', action='help', help='Show this help message and exit.')
    opts.add_option('-v', '--verbose', help='Be verbose.', default=False, action='store_true')
    opts.add_option('-t', '--target', default=None, type='int', help='Restrict to specific monitor.')
    opts.add_option('-c', '--command', default=None, help='Command to change wallpaper.', type='choice', choices=WALLPAPER_COMMANDS)
    opts.add_option('-r', '--refresh', help='Refresh the display.', default=False, action='store_true')
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
