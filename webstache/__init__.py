#!/usr/bin/env python

# webstache - static site generator
# Copyright (C) 2013-2014 Erik Edrosa
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import glob
import json
from distutils import dir_util

from webstache.generator import generate

class Webstache:
    def __init__(self, config, directory):
        self.host = config['host']
        self.title = config['title']
        self.author = config['author']
        self.header = config['header']
        self.post_limit = config['post_limit']
        self.layout_dir = os.path.join(directory, config['layout_dir'])
        self.blog_dir = os.path.join(directory, config['blog_dir'])
        self.output_dir = os.path.join(directory, config['output_dir'])

def file_not_found(filename, directory):
    sys.stderr.write('%s not found in %s\n' % (filename, directory))
    sys.exit(1)

def read_config(config_path, directory):
    config_file = open(config_path)
    config = json.load(config_file)
    config_file.close()
    webstache_config = Webstache(config, directory)
    return webstache_config

def create_output_dir(path, static_dir):
    if os.path.exists(static_dir):
        dir_util.copy_tree(static_dir, path)
    elif not os.path.exists(path):
        os.mkdir(path)

def main():
    parser = argparse.ArgumentParser(
      description='Generates static webpages based off of mustache templates')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory of mustache files and data')
    parser.add_argument('--init', action='store_true',
                        help='Initialize default files and directories')
    parser.add_argument('-c', '--config', nargs='?',
                        default='config.json',
                        help='Name of config file')
    args = parser.parse_args()

    config_path = os.path.join(args.directory, args.config)

    if not os.path.exists(config_path):
        file_not_found(args.config, args.directory)

    config = read_config(config_path, args.directory)
    
    print('Creating webpages from %s' % args.directory)
    generator.generate(config)


if __name__ == '__main__':
    main()
