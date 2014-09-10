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

def generate(path, content, template, page_paths):
    pages = [(base_name(file), load_page(file)) for file in page_paths]

    renderer = pystache.Renderer(escape=lambda u: u)
    parsed_template = pystache.parse(template)

    for dataname, main_content in pages:
        content['mainContent'] = main_content
        htmlfile = open(os.path.join(path, dataname + '.html'), 'w')
        htmlfile.write(renderer.render(parsed_template, content))
        htmlfile.close()
