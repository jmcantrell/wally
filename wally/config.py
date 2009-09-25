import os
import pathutils
from imageutils import color
from scriptutils.config import SingleConfig

from . import __appname__

class Config(SingleConfig):

    def __init__(self):
        SingleConfig.__init__(self,
                filename=os.path.join(
                    os.path.expanduser('~/.%s' % __appname__.lower()),
                    'main.cfg'
                    ),
                base={
                    'app:main': {
                        'background_color': '#000000',
                        'exclusions': [],
                        },
                    'directories': {
                        'scale': ['/usr/share/backgrounds'],
                        },
                    })

    def _get_background_color(self):
        return color.hex_to_rgb(self.get('app:main', 'background_color', '#000000'))

    def _set_background_color(self, value):
        self.set('app:main', 'background_color', color.rgb_to_hex(value))

    background_color = property(_get_background_color, _set_background_color)

    def _get_directories(self):
        dirs = {}
        for wt in self.options('directories'):
            dirs[wt] = [pathutils.expand(d) for d in self.getlist('directories', wt, [])]
        return dirs

    def _set_directories(self, directories):
        for wt, dirs in directories.iteritems():
            self.set('directories', wt, [pathutils.condense(d) for d in dirs])

    directories = property(_get_directories, _set_directories)

    def _get_exclusions(self):
        return self.getlist('app:main', 'exclusions', [])

    def _set_exclusions(self, exclusions):
        self.set('app:main', 'exclusions', exclusions)

    exclusions = property(_get_exclusions, _set_exclusions)
