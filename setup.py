#!/usr/bin/env python

from setuptools import setup

setup(name='webstache',
      version='0.1',
      description='webstache is a command line program which generates static webpages using mustache',
      author='Erik Edrosa',
      author_email='erik.edrosa@gmail.com',
      url='https://github.com/OrangeShark/webstache',
      license='GPLv3',
      scripts=['webstache/webstache.py'],
      install_requires=['pystache', 
                        'markdown'],
      entry_points = {
        'console_scripts': [
          'webstache = webstache:main'
        ],
      }
     )
