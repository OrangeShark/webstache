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
import getopt 
import argparse
import glob 
import json
from distutils import dir_util

import pystache
import markdown

def last(xs):
    return xs[-1]

def first(xs):
    return xs[0]

def remove_path(filename):
    return last(os.path.split(filename))

def remove_type(filename):
    return first(filename.split("."))

def base_name(filename):
    return remove_type(remove_path(filename))

def load_page(filename):
    return markdown.markdown(open(filename).read())

def file_not_found(filename, directory):
    sys.stderr.write('%s not found in %s\n' % filename, directory)
    sys.exit(1)

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
        file_not_fouond(args.config, args.directory)

    config_file = open(config_path)
    config = json.load(config_file)
    config_file.close()

    print('Creating webpages from %s' % args.directory)
    layouts_dir = os.path.join(args.directory, args.layouts)
    pages_dir = os.path.join(args.directory, args.pages)
    base_path = os.path.join(layouts_dir, args.base)


    if not os.path.exists(base_path):
        file_not_fouond(args.base, layouts_dir)

    template_file = open(base_path)
    template = template_file.read()
    template_file.close()
    page_paths = glob.glob(os.path.join(pages_dir, '*.md'))

    static_dir = os.path.join(args.directory, 'static')
    
    content = config['default']
    pages = [(base_name(file), load_page(file)) for file in page_paths]

    path = os.path.join(args.directory, args.output)
    if os.path.exists(static_dir):
        dir_util.copy_tree(static_dir, path)
    elif not os.path.exists(path):
        os.mkdir(path)

    renderer = pystache.Renderer()
    parsed_template = pystache.parse(template)

    for dataname, main_content in pages:
        content['mainContent'] = main_content
        htmlfile = open(os.path.join(path, dataname + '.html'), 'w')
        htmlfile.write(renderer.render(parsed_template, content))
        htmlfile.close()


if __name__ == '__main__':
    main()
