import os, re, random
from scriptutils.cache import Cache
from imageutils import find_images
from imageutils.size import aspect_ratio
from imageutils.compose import paste_scale
from gnomeutils import Background
from PIL import Image

from .config import Config
from .utils import matches_any, matches_all
from . import ASPECT_RATIOS

# FUNCTIONS {{{1

def find_wallpapers(directories): #{{{2
    wallpapers = []
    for d in directories:
        wallpapers.extend(find_images(d))
    return wallpapers

def display_type(monitor): #{{{2
    return ASPECT_RATIOS.get(aspect_ratio(monitor[0:2]), 'standard')


# CLASSES {{{1

class Wally(object): #{{{2

    def __init__(self):
        self.changer = Background()
        self.monitors = self.changer.get_monitors()
        self.config = Config()
        self.cache = Cache(os.path.join(self.config.directory, 'cache'))
        del(self.searches)
        del(self.exclusions)
        self.add_exclusions(self.config.exclusions)
        self.load_display()
        self.load_wallpapers()

    def add_search(self, pattern):
        self.search_patterns.append(re.compile(pattern, re.I))

    def add_searches(self, patterns):
        for pattern in patterns: self.add_search(pattern)

    def _get_searches(self):
        return [r.pattern for r in self.search_patterns]

    def _set_searches(self, patterns):
        del(self.searches)
        self.add_searches(patterns)

    def _del_searches(self):
        self.search_patterns = []

    searches = property(_get_searches, _set_searches, _del_searches)

    def add_exclusion(self, pattern):
        self.exclusion_patterns.append(re.compile(pattern, re.I))

    def add_exclusions(self, patterns):
        for pattern in patterns: self.add_exclusion(pattern)

    def _get_exclusions(self):
        return [r.pattern for r in self.exclusion_patterns]

    def _set_exclusions(self, patterns):
        del(self.exclusions)
        self.add_exclusions(patterns)

    def _del_exclusions(self):
        self.exclusion_patterns = []

    exclusions = property(_get_exclusions, _set_exclusions, _del_exclusions)

    def load_display(self):
        self.display = [None] * len(self.monitors)
        self.display_key = [None] * len(self.monitors)
        self.display_type = [None] * len(self.monitors)
        for n, monitor in enumerate(self.monitors):
            self.display_type[n] = display_type(monitor)
            self.display_key[n] = 'display-%s-%s' % (n, self.display_type[n])
            self.display[n] = self.cache.get(self.display_key[n])

    def load_wallpapers(self):
        self.wallpapers_all = {}
        for dt, directories in self.config.directories.items():
            self.wallpapers_all[dt] = sorted(find_wallpapers(directories))
        self.refresh_wallpapers()

    def refresh_wallpapers(self):
        self.wallpapers = {}
        for dt, wallpapers in self.wallpapers_all.items():
            self.wallpapers[dt] = [w for w in wallpapers if self.valid_wallpaper(w)]

    def dump_display(self):
        for n, wallpaper in enumerate(self.display):
            self.cache[self.display_key[n]] = wallpaper
        fn = os.path.join(self.config.directory, 'wallpaper.png')
        self.display_image.save(fn)
        self.changer.set_background(fn)
        self.cache.dump()

    def image(self, size):
        return Image.new('RGB', size, self.config.background_color)

    def valid_wallpaper(self, wallpaper):
        if self.exclusions and matches_any(wallpaper, self.exclusion_patterns): return False
        if self.searches and not matches_all(wallpaper, self.search_patterns): return False
        return True

    def change_random(self, target=None):
        for n in range(len(self.display)):
            if target is not None and target != n: continue
            self.display[n] = random.choice(self.wallpapers[self.display_type[n]])

    def refresh_display(self):
        self.display_image = self.image(self.changer.get_screen_size())
        for n, monitor in enumerate(self.monitors):
            self.set_wallpaper(n, self.display[n])
        self.dump_display()

    def set_wallpaper(self, n, wallpaper):
        monitor = self.monitors[n]
        base = self.image(monitor[0:2])
        if wallpaper and os.path.isfile(wallpaper):
            self.display_image.paste(paste_scale(base, Image.open(wallpaper)), monitor[2:4])
        else:
            self.display_image.paste(base, monitor[2:4])

    def increment(self, n, count):
        if count == 0: return
        wallpapers = self.wallpapers[self.display_type[n]]
        total = len(wallpapers)
        if total == 0: return
        count %= total
        next_idx = (-1 if count > 0 else total) + count
        wallpaper = self.display[n]
        if not wallpaper:
            wallpaper = wallpapers[next_idx]
            next_idx += count / abs(count)
        else:
            if wallpaper in wallpapers:
                idx = wallpapers.index(wallpaper) + count
            else:
                idx = 0 if count > 0 else -1
            if idx >= total: idx -= total
            wallpaper = wallpapers[idx]
        self.display[n] = wallpaper

    def change_next(self, target=None):
        for n in range(len(self.display)):
            if target is not None and target != n: continue
            self.increment(n, 1)

    def change_prev(self, target=None):
        for n in range(len(self.display)):
            if target is not None and target != n: continue
            self.increment(n, -1)
