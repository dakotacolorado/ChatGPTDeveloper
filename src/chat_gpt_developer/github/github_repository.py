from dataclasses import dataclass
from typing import List
from github import Github, InputGitTreeElement
import github
import json


class File:
    """Represents a file in a GitHub repository."""

    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content


def files_from_json(json_str: str) -> List[File]:
    """
    Creates a list of File objects from a json string.

    Args:
        json_str (str): The JSON string to convert.

    Returns:
        List[File]: The list of File objects.
    """
    json_data = json.loads(json_str)
    return [File(path=item['path'], content=item['content']) for item in json_data]


class GitHubRepository:
    def __init__(self, user: str, repository_name: str, mainline_branch: str, development_branch: str, token: str):
        self.g = Github(token)
        self.user = user
        self.repo = self.g.get_user().get_repo(repository_name)
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch

    def submit_pull_request(self, files: List[File], title: str, body: str):
        """
        Submits a pull request to the repository with the given files.

        Args:
            files (List[File]): A list of File objects representing the files to commit.
            title (str): The title of the pull request.
            body (str): The body description of the pull request.

        Returns:
            PullRequest: The created pull request object.
        """
        # Implementation here

    def get_repo_contents(self) -> List[File]:
        """
        Retrieves the list of files in the repository.

        Returns:
            List[File]: A list of File objects.
        """
        # Implementation here
