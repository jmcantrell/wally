#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
        name='Wally',
        version='0.3.12',
        description='Tool for managing desktop backgrounds.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: X11 Applications :: Gnome',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Desktop Environment :: Gnome',
            ],
        install_requires=[
            'ScriptUtils>=0.3',
            'GNOMEUtils>=0.1.5',
            'GTKUtils>=0.1.3',
            'ImageUtils>=0.1.1',
            'PathUtils>=0.6',
            ],
        entry_points={
            'console_scripts': [
                'wally=wally:main_console',
                ],
            'gui_scripts': [
                'wally-gui=wally:main_gui',
                ],
            },
        packages=[
            'wally',
            ],
        package_data={
            'wally': [
                'icons/*.svg',
                ],
            },
        )
