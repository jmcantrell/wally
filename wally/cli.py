from . import Wally

def main(opts, args):
    w = Wally()
    if opts.search: w.searches = opts.search
    if opts.exclude: w.exclusions = opts.exclude
    w.refresh_wallpapers()
    if opts.command: getattr(w, 'change_%s' % opts.command)(opts.target)
    if opts.verbose: print '\n'.join(w.display)
    if opts.command or opts.refresh: w.refresh_display()
