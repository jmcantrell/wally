import os, re, random
import gnomeutils
from scriptutils.cache import Cache
from imageutils import find_images
from imageutils.size import aspect_ratio
from imageutils.compose import paste_scale
from PIL import Image

from .config import Config
from .utils import matches_any, matches_all
from . import ASPECT_RATIOS


def display_type(aspect_ratio):
    return ASPECT_RATIOS.get(aspect_ratio, 'standard')


class Wally(object): #{{{1

    def __init__(self):
        self.changer = gnomeutils.Background()
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
        self.display_type = display_type(aspect_ratio(self.changer.get_screen_size()))
        self.display_key = 'display-%s' % self.display_type
        self.display = [None] * len(self.monitors)
        dp = self.cache.get(self.display_key, [])
        for n in range(len(self.display)):
            try:
                self.display[n] = dp[n]
            except IndexError:
                self.display[n] = None

    def load_wallpapers(self):
        self.wallpapers_all = []
        for d in self.config.directories.get(self.display_type, []):
            self.wallpapers_all.extend(find_images(d))
        self.wallpapers_all.sort()
        self.refresh_wallpapers()

    def refresh_wallpapers(self):
        self.wallpapers = [w for w in self.wallpapers_all if self.valid_wallpaper(w)]

    def dump_display(self):
        if any(self.display): self.cache[self.display_key] = self.display
        fn = os.path.join(self.config.directory, '%s.png' % self.display_key)
        self.display_image.save(fn)
        self.changer.set_background(fn)
        self.cache.dump()

    def image(self, size):
        return Image.new('RGB', size, self.config.background_color)

    def valid_wallpaper(self, wallpaper):
        if self.exclusions and matches_any(wallpaper, self.exclusion_patterns): return False
        if self.searches and not matches_all(wallpaper, self.searche_patterns): return False
        return True

    def change_random(self, target=None):
        for n in range(len(self.display)):
            if target is not None and target != n: continue
            self.display[n] = random.choice(self.wallpapers)

    def refresh_display(self):
        self.display_image = self.image(self.changer.get_screen_size())
        for n, monitor in enumerate(self.monitors):
            self.set_wallpaper(self.display[n], monitor)
        self.dump_display()

    def set_wallpaper(self, wallpaper, monitor):
        base = self.image(monitor[0:2])
        if wallpaper and os.path.isfile(wallpaper):
            self.display_image.paste(paste_scale(base, Image.open(wallpaper)), monitor[2:4])
        else:
            self.display_image.paste(base, monitor[2:4])

    def increment(self, count, target=None):
        if count == 0: return
        total = len(self.wallpapers)
        count %= total
        next_idx = (-1 if count > 0 else total) + count
        for n, m in enumerate(self.monitors):
            if target is not None and target != n: continue
            wallpaper = self.display[n]
            if not wallpaper:
                wallpaper = self.wallpapers[next_idx]
                next_idx += count / abs(count)
            else:
                if wallpaper in self.wallpapers:
                    idx = self.wallpapers.index(wallpaper) + count
                else:
                    idx = 0 if count > 0 else -1
                if idx >= total: idx -= total
                wallpaper = self.wallpapers[idx]
            self.display[n] = wallpaper

    def change_next(self, target=None):
        self.increment(1, target)

    def change_prev(self, target=None):
        self.increment(-1, target)
