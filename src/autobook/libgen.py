from autobook.core.constants import PATH_CWD
from autobook.core.frame import LibgenDataFrame
from autobook.core.models.abstract.errors import AutoBookError
from grab_fork_from_libgen import LibgenSearch
from grab_fork_from_libgen.exceptions import LibgenError
from typing_extensions import Literal


class Libgen:
    """
    A class used to represent a Libgen search.

    Attributes
    ----------
    q : str
        The query string to search for.
    topic : str, optional
        The topic to search in. Can be either 'fiction' or 'sci-tech'.
        Default is 'fiction'.

    Raises
    ------
    AutoBookError
        If no query string is provided.
    """

    def __init__(
        self,
        q=None,
        topic: Literal["fiction", "sci-tech"] = "fiction",
        clean: bool = True,
    ):
        """
        Constructs a new Libgen object.

        Parameters
        ----------
        q : str, optional
            The query string to search for.
        topic : str, optional
            The topic to search in. Can be either 'fiction' or 'sci-tech'.
            Default is 'fiction'.
        clean : bool, optional
            If true, it will try to remove trailing ISBN text from title column.
            Default is False.

        Raises
        ------
        AutoBookError
            If no query string is provided.
        """
        if not q:
            raise AutoBookError("You need to enter a query string")
        self.q = q
        self.topic = topic
        self.clean = clean

        self.results_df = None
        self.filtered_results = None

    def search(self):
        """
        Performs a search on Libgen.

        Returns
        -------
        DataFrame
            A DataFrame containing the search results.
        LibgenSearch
            The LibgenSearch object used to perform the search.
        """
        self.res = LibgenSearch(self.topic, q=self.q, language="English")
        self.results_df = LibgenDataFrame(list(self.res.get_results().values()))
        if self.clean:
            self.results_df.clean_title()

        return self

    def get_dataframe(self):
        """
        Returns the search results.

        Raises
        ------
        AutoBookError
            If no search has been performed.
        """
        if self.results_df is None:
            raise AutoBookError(
                "You need to run .search() before accessing the results"
            )
        return self.results_df

    def get_df(self):
        """
        Alias for get_dataframe method.
        Returns the search results.

        Raises
        ------
        AutoBookError
            If no search has been performed.
        """
        return self.get_dataframe()

    def filter_by_author_and_title(
        self, author: str | None = None, title: str | None = None
    ):
        # Initialize an empty list to store matching books
        matching_books = []

        # Generate variations of the author's name if author is provided
        author_variations = []
        if author:
            first_name, last_name = author.split()
            author_variations = [
                f"{first_name} {last_name}",
                f"{last_name}, {first_name}",
            ]

        # Try to get the book for each variation of the author's name and title
        for book in self.res.get_results().values():
            actual_title = book["title"]
            actual_author = book["author(s)"]
            if (
                not author
                or any(
                    author_name == actual_author
                    for author_name in author_variations
                )
            ) and (not title or title in actual_title):
                filters = {"author(s)": actual_author, "title": actual_title}
                try:
                    matching_book = res.get(
                        save_to=PATH_CWD / "books", **filters
                    )
                    if matching_book:
                        matching_books.append(matching_book)
                except LibgenError:
                    continue

        # If no book was found for any variation of the author's name and title, raise an error
        if not matching_books:
            raise LibgenError("No book matches the given author and/or title.")

        return matching_books

    def get_filtered_results(self):
        """
        Returns the filtered results.

        Raises
        ------
        AutoBookError
            If no filter has been applied.
        """
        if self.filtered_results is None:
            raise AutoBookError(
                "You need to run .filter() before getting the filtered results"
            )
        return self.filtered_results
