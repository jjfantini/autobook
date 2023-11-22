import logging
import os
import warnings
from pathlib import Path

import pandas as pd
import requests
from autobook.core.constants import PATH_CWD
from autobook.core.frame import LibgenDataFrame
from autobook.core.models.abstract.errors import AutoBookError
from grab_fork_from_libgen import LibgenSearch, Metadata
from typing_extensions import Literal

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        q: str | None = None,
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
        self.res = LibgenSearch(
            self.topic, q=self.q, language="English", format="epub"
        )
        self.results_df = LibgenDataFrame(list(self.res.get_results().values()))

        if self.clean:
            self._clean_title()

        return self

    def _clean_title(self):
        """
        Cleans the title column by extracting all the text before 'ISBN:' for each row in the dataframe.
        """
        self.results_df["title"] = self.results_df["title"].apply(
            lambda x: x.split("ISBN:", 1)[0]
        )
        return self

    def get_df(self):
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
            author_mask = self.results_df["author(s)"].str.contains(
                author_regex, case=False, regex=True
            )
        else:
            author_mask = pd.Series([True] * len(self.results_df))
        if title:
            title_mask = self.results_df["title"].str.contains(
                title, case=False, regex=True
            )
        else:
            title_mask = pd.Series([True] * len(self.results_df))
        self.filtered_results_df = self.results_df[author_mask & title_mask]
        return self

    def get_filtered_df(self):
        """
        Returns the filtered results.

        Raises
        ------
        AutoBookError
            If no filter has been applied.
        """
        if self.filtered_results_df is None:
            raise AutoBookError(
                "You need to run .filter() before getting the filtered results"
            )
        return self.filtered_results_df

    def download_file(
        self,
        row: LibgenDataFrame | None = None,
        download_path: Path = PATH_CWD / "books",
    ):
        """
        Downloads a file from an available mirror URL in the filtered results.

        Parameters
        ----------
        download_path : str
            The path to save the downloaded file.
        row : LibgenDataFrame
            A single row of a dataframe that has been selected to be downloaded

        Returns
        -------
        str
            A message indicating the result of the download attempt.
        """
        if row is None:
            warnings.warn(
                "No row selected. Using the first row in search results",
                stacklevel=1,
            )
            md5 = self.results.iloc[0:1]["md5"].values[0]
        else:
            md5 = row["md5"].values[0]

        download_urls = Metadata(timeout=(10, 20)).get_download_links(
            md5, topic="fiction"
        )

        for url in download_urls:
            if self._is_link_available(url):
                return self._download_from_url(url, download_path)
                break

        return "No available mirrors to download from."

    def _is_link_available(self, url) -> bool:
        """
        Checks if the mirror URL is available.

        Parameters
        ----------
        url : str
            The URL of the mirror to check.

        Returns
        -------
        bool
            True if the mirror is available, False otherwise.
        """
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _download_from_url(self, url, download_path):
        """
        Downloads a file from the given URL.

        Parameters
        ----------
        url : str
            The URL to download the file from.
        download_path : str
            The path to save the downloaded file.

        Returns
        -------
        str
            A message indicating the result of the download attempt.
        """
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = url.split("/")[-1]
                full_path = os.path.join(download_path, file_name)
                with open(full_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                return f"Download successful: {full_path}"
            else:
                return "Error: Unable to download file from the URL."
        except requests.RequestException as e:
            raise AutoBookError(f"Error: {e}") from e
