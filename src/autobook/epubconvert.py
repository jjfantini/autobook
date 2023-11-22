from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


class EpubConvert:
    """
    A class used to convert epub files to text files.

    ...

    Attributes
    ----------
    path : str
        a string representing the path of the epub file
    book : epub.EpubBook
        an EpubBook object representing the epub file
    book_items : list
        a list of EpubItem objects in the epub file
    book_chapters : list
        a list of EpubItem objects that represent chapters in the epub file

    Methods
    -------
    epub_to_txt(fileOut: str)
        Converts the chapters in the epub file to a text file.
    _chapter_to_str(chapter)
        Converts a chapter in the epub file to a string. ONLY for use in
        epub_to_txt()
    """

    def __init__(self, fileIn):
        """
        Constructs all the necessary attributes for the EpubConvert object.

        Parameters
        ----------
        fileIn : str
            a string representing the path of the epub file
        """
        self.path = fileIn
        self.book = epub.read_epub(fileIn)
        self.book_items = list(self.book.get_items_of_type(ITEM_DOCUMENT))
        self.book_chapters = [
            item for item in self.book_items if "ch" in item.get_name()
        ]

    def epub_to_txt(self, fileOut: str):
        """
        Converts the chapters in the epub file to a text file.

        Parameters
        ----------
        fileOut : str
            a string representing the path of the output text file

        Returns
        -------
        EpubConvert
            the EpubConvert object itself
        """
        texts = {}
        for chapter in self.book_chapters:
            texts[chapter.get_name()] = self._chapter_to_str(chapter)
        compiled_text = """


        """.join(
            texts.values()
        )

        # Save the file
        with open(fileOut, "w", encoding="utf-8") as f:
            f.write(compiled_text)
        return self

    def _chapter_to_str(self, chapter):
        """
        Converts a chapter in the epub file to a string.

        Parameters
        ----------
        chapter : epub.EpubHtml
            an EpubHtml object representing a chapter in the epub file

        Returns
        -------
        str
            a string representing the chapter
        """
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        h1 = [header.get_text() for header in soup.find_all("h1")]
        h2 = [header.get_text() for header in soup.find_all("h2")]
        h3 = [header.get_text() for header in soup.find_all("h3")]
        if h1:  # only perform h1.append if h1 is not an empty list
            if not any("Chapter" in header for header in h1):
                h1 = ["Chapter " + header for header in h1]
            h1.insert(0, "      ")  # Adding spaces to the beginning of the list
            h1.append("     ")  # Adding spaces for a pause after `Chapter One`
        if h2:  # only perform h2.append if h2 is not an empty list
            h2.insert(0, "      ")  # Adding spaces to the beginning of the list
            h2.append(
                """


            """
            )  # Adding spaces for a pause after h2
        if h3:  # only perform h3.append if h3 is not an empty list
            h3.insert(0, "      ")  # Adding spaces to the beginning of the list
            h3.append(
                """


            """
            )  # Adding spaces for a pause after h3
        text = [para.get_text() for para in soup.find_all("p")]
        return "".join(h1 + h2 + h3 + text)
