import ebooklib
from ebooklib import epub


class EpubConvert:
    def __init__(self, path):
        self.path = path
        self.epub = epub.read_epub(path)
