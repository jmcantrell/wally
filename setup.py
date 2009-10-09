#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
        name='Wally',
        version='0.6.1',
        description='Tool for managing desktop backgrounds.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: X11 Applications :: Gnome',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Desktop Environment :: Gnome',
            ],
        install_requires=[
            'ScriptUtils',
            'GNOMEUtils',
            'GTKUtils',
            'ImageUtils',
            'PathUtils',
            ],
        entry_points={
            'console_scripts': [
                'wally=wally.console:main',
                ],
            'gui_scripts': [
                'wally-gui=wally.gui:main',
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
