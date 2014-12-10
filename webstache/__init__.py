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

from webstache import generator

def file_not_found(filename, directory):
    sys.stderr.write('%s not found in %s\n' % (filename, directory))
    sys.exit(1)

def read_config(config_path):
    config_file = open(config_path)
    config = json.load(config_file)
    config_file.close()
    return config

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
    parser.add_argument('-o', '--output', nargs='?', default='out',
                        help='Name of directory to store the output')
    parser.add_argument('-l', '--layouts', nargs='?',
                        default='layouts/',
                        help='Directory of layout files')
    parser.add_argument('-p', '--pages', nargs='?',
                        default='pages/',
                        help='Directory of pages')
    parser.add_argument('-c', '--config', nargs='?',
                        default='config.json',
                        help='Name of config file')
    parser.add_argument('-b', '--base', nargs='?',
                        default='base.html.mustache',
                        help='Name of the base layout')
    args = parser.parse_args()

    config_path = os.path.join(args.directory, args.config)

    if not os.path.exists(config_path):
        file_not_found(args.config, args.directory)

    config = read_config(config_path)

    layouts_dir = os.path.join(args.directory, args.layouts)
    pages_dir = os.path.join(args.directory, args.pages)
    template_base_path = os.path.join(layouts_dir, args.base)

    if not os.path.exists(template_base_path):
        file_not_found(args.base, layouts_dir)
    
    static_dir = os.path.join(args.directory, 'static')
    output_path = os.path.join(args.directory, args.output)
    create_output_dir(output_path, static_dir)

    content = config['default']
   
    print('Creating webpages from %s' % args.directory)
    generator.generate(pages_dir, template_base_path, content, output_path)


if __name__ == '__main__':
    main()
