
import pandas as pd
from autobook.core.frame import LibgenDataFrame
from autobook.core.models.abstract.errors import AutoBookError
from grab_fork_from_libgen import LibgenSearch
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

    def __init__(self, q=None, topic: Literal["fiction", "sci-tech"] = "fiction"):
        """
        Constructs a new Libgen object.

        Parameters
        ----------
        q : str, optional
            The query string to search for.
        topic : str, optional
            The topic to search in. Can be either 'fiction' or 'sci-tech'.
            Default is 'fiction'.

        Raises
        ------
        AutoBookError
            If no query string is provided.
        """
        if not q:
            raise AutoBookError("You need to enter a query string")
        self.q = q
        self.topic = topic

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
        res_ol = self.res.get_results()
        self.results = LibgenDataFrame(list(res_ol.values()))
        return self

    def filter(self, author=None, title=None):
        """
        Filters a libgen df based on author and title, created by  `query`.

        Parameters
        ----------
        df : DataFrame
            The dataframe to filter.
        author : str, optional
            The author to filter by. If not provided, no filtering is done based
            on author.
        title : str, optional
            The title to filter by. If not provided, no filtering is done based
            on title.

        Returns
        -------
        DataFrame
            The filtered dataframe.
        """
        if author:
            # Split the author string into words and create a regex pattern that
            # matches either 'word1 word2' or 'word2, word1'
            words = author.split()
            author_regex = f"{words[0]} {words[1]}|{words[1]}, {words[0]}"
            author_mask = self.results["author(s)"].str.contains(
                author_regex, case=False, regex=True
            )
        else:
            author_mask = pd.Series([True] * len(self.results))
        if title:
            title_mask = self.results["title"].str.contains(title, case=False, regex=True)
        else:
            title_mask = pd.Series([True] * len(self.results))
        filtered_df = self.results[author_mask & title_mask]
        return filtered_df

