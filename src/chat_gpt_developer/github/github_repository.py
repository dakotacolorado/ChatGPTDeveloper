from dataclasses import dataclass
from typing import List
from github import Github, InputGitTreeElement
import github
import json


@dataclass(frozen=True)
class File:
    """Represents a file in a GitHub repository."""
    path: str
    content: str


def files_from_json(json_str: str) -> List[File]:
    """
    Creates a list of File instances from a JSON string.

    Args:
        json_str: A JSON string representing a list of files.

    Returns:
        A list of File instances.
    """
    return [
        File(path=file["path"], content=file["content"])
        for file in json.loads(json_str)
    ]

class GitHubRepository:
    def __init__(self, token: str, repository_name: str, mainline_branch: str, development_branch: str) -> None:
        """
        Initializes a GitHubRepository instance.

        Args:
            token: GitHub access token for authentication.
            repository_name: Name of the repository to work with.
            mainline_branch: Name of the mainline branch in the repository, typically 'main'.
            development_branch: Name of the development branch in the repository.
        """
        self.g = Github(token)
        self.repo = self.g.get_repo(repository_name)
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch

    def submit_pull_request(self, files: List[File], title: str, body: str) -> github.PullRequest:
        """
        Submits a pull request to the repository with the given files.

        Args:
            files: A list of File instances representing the files to commit.
            title: The title of the pull request.
            body: The body description of the pull request.

        Returns:
            The created pull request object.
        """
        # Retrieve the latest commit from the mainline branch
        mainline_commit = self.repo.get_branch(self.mainline_branch).commit.commit

        try:
            # Try getting the development branch
            self.repo.get_branch(self.development_branch)
        except github.GithubException:
            # If it doesn't exist, create it
            self.repo.create_git_ref(f'refs/heads/{self.development_branch}', mainline_commit.sha)
        
        # Create the base tree from the mainline commit
        base_tree = self.repo.get_git_tree(mainline_commit.sha)

        # Prepare the list of tree elements for the new commit
        element_list = [InputGitTreeElement(path=file.path, mode='100644', type='blob', content=file.content) for file in files]
        # Create a new tree
        new_tree = self.repo.create_git_tree(element_list, base_tree)

        # Create a new commit
        commit_message = title
        new_commit = self.repo.create_git_commit(commit_message, new_tree, [mainline_commit])
        # Update the development branch to point to the new commit
        self.repo.get_git_ref(f'heads/{self.development_branch}').edit(new_commit.sha)

        # Create and return the new pull request
        return self.repo.create_pull(title=title, body=body, head=self.development_branch, base=self.mainline_branch)

    def get_repo_contents(self) -> List[File]:
        """
        Retrieves a list of file metadata from the repository.

        Returns:
            A list of File instances representing the files in the repository.
        """
        file_list = []
        contents = self.repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                file_data = self.repo.get_contents(file_content.path)
                file_list.append(File(path=file_content.path, content=file_data.decoded_content.decode()))

        return file_list
