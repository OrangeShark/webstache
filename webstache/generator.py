# Generators for webpages
# Copyright (C) 2013-2015 Erik Edrosa
#
# This file is part of webstache
# 
# webstache is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# webstache is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with webstache. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import itertools
import os
import sys
import glob

import pystache
import markdown
import PyRSS2Gen as RSS2

from webstache.blogpost import (Post, parse_post_file)
from webstache.page import Page

def create_dir_if_needed(file_path):
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def read_template(base_path):
    template_file = open(base_path)
    template = pystache.parse(template_file.read())
    template_file.close()
    return template

def parse_post(md, post_file):
    html = md.convert(post_file.read())
    return md.Meta['title'][0], md.Meta['date'][0], md.Meta['tags'][0].split(', '), html

def create_post(md, post_path):
    post_file = open(post_path)
    title, date, tags, content = parse_post(md, post_file)
    return Post(post_path, title, date, tags, content)

def generate(config):
    page_template = read_template(os.path.join(config.layout_dir, 'page.mustache'))
    post_template = read_template(os.path.join(config.layout_dir, 'post.mustache'))
    md = markdown.Markdown(extensions = ['markdown.extensions.meta',
                                         'markdown.extensions.fenced_code',
                                         'markdown.extensions.codehilite'])
    # Don't escape html
    renderer = pystache.Renderer(escape=lambda u: u)
    post_paths = glob.glob(os.path.join(config.blog_dir, '*.md'))
    post_paths.sort(reverse=True)
    
    posts = [create_post(md, post) for post in post_paths]

    generate_index(renderer, page_template, config, posts)
    # generate posts pages
    def create_page(post, content):
        page = Page(post.src, config.host, config.title + ' - ' + post.title, 
                    config.author, config.header, content)
        page.uri = post.uri()
        return page

    blog_pages = map(create_page, posts, generate_blog(renderer, post_template, posts))
    for page in blog_pages:
        page_path = os.path.join(config.output_dir, page.uri)
        create_dir_if_needed(page_path)
        page_file = open(page_path, 'w')
        page_file.write(renderer.render(page_template, page))
        page_file.close()

    generate_rss_feed(config, posts)

def generate_index(renderer, page_template, config, posts):
    index_post_template = read_template(os.path.join(config.layout_dir, 'indexpost.mustache'))
    # generate posts for the index
    blog_posts = generate_blog(renderer, index_post_template, posts)
    index_blog_posts = list(itertools.islice(blog_posts, config.post_limit))
    page_num = 1
    prev_page = None

    while index_blog_posts:
        content = '\n'.join([post for post in index_blog_posts])
        index_page = Page( (page_num == 1 and "index") or ("index-" + str(page_num)), 
                           config.host, config.title, config.author, 
                           config.header, content)
        # link pages together
        if prev_page:
            index_page.prev_page = prev_page
            prev_page.next_page = index_page

        index_blog_posts = list(itertools.islice(blog_posts, config.post_limit))
        prev_page = index_page
        page_num += 1

    while prev_page:
        index_page = prev_page
        prev_page = index_page.prev_page

        index_page_uri = index_page.uri()
        index_path = os.path.join(config.output_dir, index_page_uri)
        create_dir_if_needed(index_path)
        index_file = open(index_path, 'w')
        index_file.write(renderer.render(page_template, index_page))
        index_file.close()


def generate_pages(renderer, page_template, pages):
    pass

def generate_blog(renderer, post_template, posts):
    def generate_post(post):
        return renderer.render(post_template, post)

    return map(generate_post, posts)

def generate_rss_feed(config, posts):
    def generate_item(post):
        url = config.host + post.uri()
        return RSS2.RSSItem(
            title = post.title,
            link = url,
            description = post.content,
            guid = RSS2.Guid(url),
            pubDate = post._date)

    rss = RSS2.RSS2(
        title = config.title,
        link = config.host,
        description = config.description,
        lastBuildDate = datetime.now(),
        items = map(generate_item, posts))
    
    rss_path = os.path.join(config.output_dir, 'feed.xml')
    
    rss.write_xml(open(rss_path, 'w'))
