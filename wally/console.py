import pathutils
from scriptutils.options import Options
from . import Wally, utils
from . import WALLPAPER_ACTIONS, WALLPAPER_TYPES

def split_opt(opt):
    return [o.strip() for o in opt.split(',')]

def get_options(): #{{{1
    opts = Options('Usage: %prog [options]', width=35)
    opts.add_option('-h', '--help', action='help',
            help='Show this help message and exit.')
    opts.add_option('-v', '--verbose', help='Be verbose.',
            default=False, action='store_true')
    opts.add_option('-t', '--target', default=None, type='int',
            help='Restrict to specific monitor.')
    opts.add_option('-c', '--command', default=None,
            help='Command to change wallpaper.', type='choice',
            choices=WALLPAPER_ACTIONS)
    opts.add_option('-r', '--refresh', help='Refresh the display.',
            default=False, action='store_true')
    opts.add_option('-s', '--search', metavar='REGEX',
            help='Search filenames based on REGEX.')
    opts.add_option('-x', '--exclude', metavar='REGEX',
            help='Exclude filenames based on REGEX.')
    opts.add_option('-T', '--types', metavar='TYPES',
            help='Use specified wallpaper types (comma-separated).',
            choices=WALLPAPER_TYPES)
    opts.add_option('-D', '--directories', metavar='DIRS',
            help='Use specified directories (comma-separated).')

    return opts.parse_args()

def main(): #{{{1
    opts, args = get_options()
    kwargs = {}
    if opts.types:
        kwargs['types'] = split_opt(opts.types)
        if opts.directories:
            kwargs['directories'] = {kwargs['types'][0]: [pathutils.expand(d) for d in split_opt(opts.directories)]}
    w = Wally(**kwargs)
    if opts.search: w.add_search(opts.search)
    if opts.exclude: w.add_exclusion(opts.exclude)
    w.refresh_wallpapers()
    if opts.command: getattr(w, 'change_%s' % opts.command)(opts.target)
    if opts.verbose: print '\n'.join(w[1] for w in w.wallpaper)
    if opts.command or opts.refresh: w.refresh_display()
