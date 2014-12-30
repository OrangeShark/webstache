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

import itertools
import os
import sys
import glob

import pystache
import markdown

from webstache.blogpost import (Post, parse_post_file)

def create_dir_if_needed(file_path):
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def read_template(base_path):
    template_file = open(base_path)
    template = pystache.parse(template_file.read())
    template_file.close()
    return template

def parse_post(post_file):
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    html = md.convert(post_file.read())
    return md.Meta['title'][0], md.Meta['date'][0], md.Meta['tags'][0].split(', '), html

def create_post(post_path):
    post_file = open(post_path)
    title, date, tags, content = parse_post(post_file)
    return Post(post_path, title, date, tags, content)

def generate(config):
    page_template = read_template(os.path.join(config.layout_dir, 'page.mustache'))
    index_post_template = read_template(os.path.join(config.layout_dir, 'indexpost.mustache'))
    post_template = read_template(os.path.join(config.layout_dir, 'post.mustache'))
    # Don't escape html
    renderer = pystache.Renderer(escape=lambda u: u)
    post_paths = glob.glob(os.path.join(config.blog_dir, '*.md'))
    post_paths.sort(reverse=True)

    posts = [create_post(post) for post in post_paths]
    # generate posts for the index
    blog_posts = generate_blog(renderer, index_post_template, posts, None)
    index_blog_posts = itertools.islice(blog_posts, 5)
    content = '\n'.join([post for post in index_blog_posts])

    index_path = os.path.join(config.output_dir, 'index.html')
    create_dir_if_needed(index_path)
    index_file = open(index_path, 'w')
    index_file.write(renderer.render(page_template, config, {'content': content}))
    index_file.close()
    # generate posts pages
    blog_pages = zip(map(Post.uri, posts), generate_blog(renderer, post_template, posts, None))
    for uri, page in blog_pages:
        page_path = os.path.join(config.output_dir, uri)
        create_dir_if_needed(page_path)
        page_file = open(os.path.join(config.output_dir, uri), 'w')
        page_file.write(renderer.render(page_template, config, {'content': page}))
        page_file.close()

def generate_index():
    pass

def generate_page():
    pass

def generate_blog(renderer, post_template, posts, widgets):
    def generate_post(post):
        return renderer.render(post_template, post, widgets)

    return map(generate_post, posts)
