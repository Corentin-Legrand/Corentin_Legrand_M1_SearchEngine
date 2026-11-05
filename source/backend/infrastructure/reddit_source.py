"""Fetching of documents from Reddit."""

from datetime import datetime, timezone
from typing import Any

import pandas as pd
import praw
from praw.models import Submission

from helpers.environment_manager import EnvironmentManager
from helpers.text_manager import TextManager
from models.document_origin import DocumentOrigin
from service.document_schema import DocumentColumn
from service.interfaces.i_document_source import IDocumentSource

REDDIT_CLIENT_ID_KEY: str = "REDDIT_CLIENT_ID"
REDDIT_CLIENT_SECRET_KEY: str = "REDDIT_CLIENT_SECRET"
REDDIT_USER_AGENT_KEY: str = "REDDIT_USER_AGENT"
REDDIT_SUBREDDIT: str = "all"
REDDIT_BASE_URL: str = "https://www.reddit.com"
REDDIT_DELETED_AUTHOR: str = "[deleted]"


class RedditSource(IDocumentSource):
    """
    Fetch Reddit posts through the praw library; the text of a post is its `selftext`.

    Attributes:
        reddit (praw.Reddit): Reddit API client (private).
        text_manager (TextManager): Helper cleaning the texts (private).

    Author: Corentin Legrand
    """

    def __init__(self) -> None:
        """Build the Reddit client from the `REDDIT_*` environment variables.

        Raises:
            EnvironmentVariableNotFoundError: If a Reddit credential is not defined.
        """
        environment: EnvironmentManager = EnvironmentManager.get_instance()
        self.__reddit: praw.Reddit = praw.Reddit(
            client_id=environment.get_environment_variable(REDDIT_CLIENT_ID_KEY),
            client_secret=environment.get_environment_variable(REDDIT_CLIENT_SECRET_KEY),
            user_agent=environment.get_environment_variable(REDDIT_USER_AGENT_KEY),
        )
        self.__text_manager: TextManager = TextManager()

    def fetch_documents(self, query: str, max_results: int) -> pd.DataFrame:
        """Search the Reddit posts matching a query.

        Args:
            query (str): The keywords to search.
            max_results (int): The maximum number of posts to fetch.

        Returns:
            pd.DataFrame: One row per post.
        """
        submissions = self.__reddit.subreddit(REDDIT_SUBREDDIT).search(query, limit=max_results)
        return pd.DataFrame([self.__build_row(submission) for submission in submissions])

    def __build_row(self, submission: Submission) -> dict[str, Any]:
        """Convert a Reddit post into a document row.

        Args:
            submission (Submission): The Reddit post.

        Returns:
            dict[str, Any]: The document row.
        """
        return {
            DocumentColumn.TITLE: self.__text_manager.to_single_line(submission.title),
            DocumentColumn.AUTHOR: str(submission.author) if submission.author else REDDIT_DELETED_AUTHOR,
            DocumentColumn.DATE: datetime.fromtimestamp(submission.created_utc, tz=timezone.utc),
            DocumentColumn.URL: f"{REDDIT_BASE_URL}{submission.permalink}",
            DocumentColumn.TEXT: self.__text_manager.to_single_line(submission.selftext),
            DocumentColumn.ORIGIN: DocumentOrigin.REDDIT.value,
            DocumentColumn.NB_COMMENTS: submission.num_comments,
        }
