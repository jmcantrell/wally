#!/usr/bin/env python

from setuptools import setup

setup(
        name='Wally',
        version='0.7.3',
        description='Tool for managing desktop backgrounds.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: X11 Applications :: Gnome',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
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
                'wally=wally.__main__:main',
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
