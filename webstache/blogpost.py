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


