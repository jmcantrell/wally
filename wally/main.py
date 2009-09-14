import os, re, random
import gnomeutils, imageutils, imageutils.compose
from scriptutils.cache import Cache
from PIL import Image

from . import WALLPAPER_TYPES, WALLPAPER_COMMANDS
from . import config, utils

class Wally(object): #{{{1

    def __init__(self):
        self.clear_searches()
        self.clear_exclusions()
        self.clear_excluded_types()
        self.excluded_types = []
        self.changer = gnomeutils.Background()
        self.monitors = self.changer.get_monitors()
        self.screen_image = None
        self.config = config.Config()
        self.cache = Cache(os.path.join(self.config.directory, 'cache'))
        self.add_exclusions(self.config.exclusions)
        self._load_wallpaper()
        self._load_wallpapers()

    def _load_wallpaper(self):
        monitor_count = len(self.monitors)
        screen_size = '%sx%s' % self.changer.get_screen_size()
        self.wallpaper_key = 'wallpaper-%s' % screen_size
        self.wallpaper_file = '%s.png' % self.wallpaper_key
        w = [None] * monitor_count
        prev_w = self.cache[self.wallpaper_key]
        if prev_w:
            prev_w.extend(w)  # just to ensure there is enough wiggle room
            for n in range(len(w)): w[n] = prev_w[n]
        self.wallpaper = w

    def _load_wallpapers(self):
        self.wallpapers_all = []
        for n, wt in enumerate(WALLPAPER_TYPES):
            if len(self.monitors) < 2 and wt == 'multi': continue
            directories = self.config.directories.get(wt)
            if not directories: continue
            wallpapers = self.find_wallpapers(directories)
            if not wallpapers: continue
            self.wallpapers_all.extend([(n, f) for f in wallpapers])
        self.wallpapers_all.sort()
        self.refresh_wallpapers()

    def refresh_wallpapers(self):
        self.wallpapers = [w for w in self.wallpapers_all
                if self.valid_wallpaper(w)]

    def get_wallpapers(self, types=None):
        if not types: types = range(len(WALLPAPER_TYPES))
        return [w for w in self.wallpapers if w[0] in types]

    def dump_wallpaper(self):
        if any(self.wallpaper):
            self.cache[self.wallpaper_key] = self.wallpaper
        w_file = os.path.join(self.config.directory, self.wallpaper_file)
        self.screen_image.save(w_file)
        self.changer.set_background(w_file)

    def base_image(self, size):
        return Image.new('RGB', size, self.config.background_color)

    def clear_searches(self):
        self.searches = []

    def add_search(self, pattern):
        self.searches.append(re.compile(pattern, re.I))

    def add_searches(self, patterns):
        for p in patterns: self.add_search(p)

    def set_searches(self, patterns):
        self.clear_searches()
        self.add_searches(patterns)

    def get_searches(self):
        return [r.pattern for r in self.searches]

    def clear_exclusions(self):
        self.exclusions = []

    def add_exclusion(self, pattern):
        self.exclusions.append(re.compile(pattern, re.I))

    def add_exclusions(self, patterns):
        for p in patterns: self.add_exclusion(p)

    def set_exclusions(self, patterns):
        self.clear_exclusions()
        self.add_exclusions(patterns)

    def get_exclusions(self):
        return [r.pattern for r in self.exclusions]

    def clear_excluded_types(self):
        self.excluded_types = []

    def add_excluded_type(self, t):
        self.excluded_types.append(WALLPAPER_TYPES.index(t))

    def add_excluded_types(self, types):
        for t in types: self.add_excluded_type(t)

    def set_excluded_types(self, types):
        self.clear_excluded_types()
        self.add_excluded_types(types)

    def get_excluded_types(self):
        return [WALLPAPER_TYPES[t] for t in self.excluded_types]

    def find_wallpapers(self, directories):
        wallpapers = []
        for directory in directories:
            wallpapers.extend(imageutils.find_images(directory))
        return wallpapers

    def get_random_wallpaper(self, types=None):
        pool = self.get_wallpapers(types)
        if not pool: return None
        return random.choice(pool)

    def valid_wallpaper(self, w):
        if w[0] in self.excluded_types:
            return False
        if self.exclusions and utils.matches_any(w[1], self.exclusions):
            return False
        if self.searches and not utils.matches_all(w[1], self.searches):
            return False
        return True

    def increment(self, count, target=None):
        if count == 0: return
        wall_count = len(self.wallpapers)
        if abs(count) > wall_count: return
        next_idx = (-1 if count > 0 else wall_count) + count
        for n, m in enumerate(self.monitors):
            if target is not None and target != n: continue
            w = self.wallpaper[n]
            if not w:
                w = self.wallpapers[next_idx]
                next_idx += count / abs(count)
            else:
                if w in self.wallpapers:
                    idx = self.wallpapers.index(w) + count
                else:
                    idx = 0 if count > 0 else -1
                if idx >= wall_count: idx -= wall_count
                w = self.wallpapers[idx]
            self.wallpaper[n] = w

    def change_random(self, target=None):
        types = range(len(WALLPAPER_TYPES))
        if target is not None:
            types.remove(WALLPAPER_TYPES.index('multi'))
        for n, m in enumerate(self.monitors):
            if target is not None and target != n: continue
            w = self.get_random_wallpaper(types)
            if not w: break
            if WALLPAPER_TYPES[w[0]] == 'multi':
                self.wallpaper = [w]
                break
            self.wallpaper[n] = w

    def change_next(self, target=None):
        self.increment(1, target)

    def change_prev(self, target=None):
        self.increment(-1, target)

    def change_multi(self, target=None):
        if len(self.monitors) < 2: return
        types = [WALLPAPER_TYPES.index('multi')]
        w = self.get_random_wallpaper(types)
        self.set_wallpaper_multi(w)

    def refresh_display(self):
        self.screen_image = self.base_image(self.changer.get_screen_size())
        for n, m in enumerate(self.monitors):
            w = self.wallpaper[n]
            if not w: continue
            if WALLPAPER_TYPES[w[0]] == 'multi':
                self.set_wallpaper_multi(w[1])
                break
            self.set_wallpaper(w, m)
        self.dump_wallpaper()

    def set_wallpaper_multi(self, w):
        base = self.base_image(self.changer.get_screen_size())
        if os.path.isfile(w):
            self.screen_image = imageutils.compose.paste_scale(base, Image.open(w))
        else:
            self.screen_image = base

    def set_wallpaper(self, w, monitor):
        paster = getattr(imageutils.compose, 'paste_%s' % WALLPAPER_TYPES[w[0]])
        base = self.base_image(monitor[0:2])
        if os.path.isfile(w[1]):
            self.screen_image.paste(
                    paster(base, Image.open(w[1])), monitor[2:4])
        else:
            self.screen_image.paste(base, monitor[2:4])

