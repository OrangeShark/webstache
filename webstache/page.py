# Page specific code
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

import os

class Page:
    def __init__(self, src, host, title, author, header, 
                 content, next_page=None, prev_page=None):
        self.src = src
        self.host = host
        self.title = title
        self.author = author
        self.header = header
        self.content = content
        self.next_page = next_page
        self.prev_page = prev_page

    def uri(self):
        file_name = os.path.basename(self.src)
        root, _ = os.path.splitext(file_name)
        return root + ".html"
