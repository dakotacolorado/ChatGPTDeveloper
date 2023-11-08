from dataclasses import dataclass
from typing import List, Optional
from github import Github, InputGitTreeElement, GithubException
from github.Repository import Repository
import json


def files_from_json(json_str: str) -> List[File]:
    """
    Creates a File list from a json string.

    Args:
        json_str (str): The JSON string containing file information.

    Returns:
        List[File]: A list of File objects.
    """
    try:
        file_data = json.loads(json_str)
        return [File(path=file['path'], content=file['content']) for file in file_data]
    except json.JSONDecodeError as err:
        raise ValueError(f'Invalid JSON passed: {err}')


class GitHubRepository:
    def __init__(self, repository: Repository, mainline_branch: str, development_branch: str, token: str) -> None:
        """
        Initializer for GitHubRepository.

        Args:
            repository (Repository): The GitHub repository object.
            mainline_branch (str): The mainline branch name.
            development_branch (str): The development branch name.
            token (str): Personal Access Token for GitHub.
        """
        self.g = Github(token)
        self.repo = repository
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch

    # ... existing methods ...

    def submit_pull_request(self, files: List[File], title: str, body: str) -> Optional[PullRequest]:
        # ... existing code ...
        return pr

    def get_repo_contents(self) -> List[File]:
        # ... existing code ...
        return file_list

@dataclass(frozen=True)
class File:
    """
    A file in a GitHub repository.

    Args:
        path (str): The path of the file.
        content (str): The content of the file.
    """
    path: str
    content: str
