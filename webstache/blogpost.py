# blog post specific definitions
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
import os
import re

class Post:
    def __init__(self, src, title, date, tags, content, date_format="%Y/%m/%d"):
        self.src = src
        self.title = title
        self._date = datetime.strptime(date, "%Y-%m-%d")
        self.tags = [{'tag': tag} for tag in tags]
        self.content = content
        self.date_format = date_format

    def date(self):
        return self._date.strftime(self.date_format)

    def uri(self):
        file_name = os.path.basename(self.src)
        date, page = parse_post_file(file_name)
        date_parts = date.split("-")
        return os.path.join(date_parts[0], date_parts[1], date_parts[2], page + '.html')

post_pattern = re.compile("^(\d{4}-\d{2}-\d{2})-(.+?)\.md$")

def parse_post_file(post_name):
    matches = re.match(post_pattern, post_name)
    return matches and matches.groups()


