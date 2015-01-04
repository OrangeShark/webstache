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
