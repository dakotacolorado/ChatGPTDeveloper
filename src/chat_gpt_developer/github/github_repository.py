from dataclasses import dataclass
from typing import Any, List
import json
from github import Github, InputGitTreeElement, GithubException


def files_from_json(json_str: str) -> List[Any]:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as err:
        raise ValueError('Invalid JSON string') from err


@dataclass(frozen=True)
class File:
    """Represents a file in a GitHub repository."""
    path: str
    content: str


class GitHubRepository:
    def __init__(self, user: str, repository_name: str, mainline_branch: str, development_branch: str, token: str) -> None:
        self.github = Github(token)
        self.user = user
        self.repo = self.github.get_user().get_repo(repository_name)
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch

    # Other methods currently remain the same
