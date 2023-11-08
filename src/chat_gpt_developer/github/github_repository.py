from dataclasses import dataclass
from typing import List, Optional
from github import Github, InputGitTreeElement
import github
import json


def files_from_json(json_str: str) -> List[File]:
    """
    Creates a list of File instances from a json string.

    Args:
        json_str: A JSON formatted string representing a list of files.

    Returns:
        A list of File instances.
    """
    return [
        File(path=file['path'], content=file['content'])
        for file in json.loads(json_str)
    ]


def to_json(files: List[File]) -> str:
    """
    Converts a list of File instances to a JSON string.

    Args:
        files: A list of File instances.

    Returns:
        A JSON formatted string representing the files.
    """
    return json.dumps([
        {'path': file.path, 'content': file.content}
        for file in files
    ], indent=4)


class GitHubRepository:
    def __init__(self, user: str, repository_name: str, mainline_branch: str, development_branch: Optional[str], token: str) -> None:
        self.g = Github(token)
        self.user = user
        self.repo = self.g.get_user().get_repo(repository_name)
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch or f'dev-{mainline_branch}'

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
        # Get the latest commit from the mainline branch
        mainline = self.repo.get_branch(self.mainline_branch).commit.commit

        # Check if development branch exists, create if it doesn't
        try:
            dev_ref = self.repo.get_git_ref(f'heads/{self.development_branch}')
        except github.GithubException:
            dev_ref = self.repo.create_git_ref(f'refs/heads/{self.development_branch}', mainline.sha)

        base_tree = self.repo.get_git_tree(mainline.sha)

        # Create new tree for the files to commit
        element_list = [
            InputGitTreeElement(
                path=file.path,
                mode='100644',
                type='blob',
                content=file.content
            )
            for file in files
        ]
        tree = self.repo.create_git_tree(element_list, base_tree)

        # Create a new commit in the repository
        commit = self.repo.create_git_commit(title, tree, [mainline])

        # Update the development branch to the new commit
        self.repo.get_git_ref(f'heads/{self.development_branch}').edit(sha=commit.sha)

        # Create the pull request
        pr = self.repo.create_pull(title=title, body=body, head=self.development_branch, base=self.mainline_branch)
        return pr

    def get_repo_contents(self) -> List[File]:
        """
        Retrieves the contents of the repository.

        Returns:
            A list of File instances representing the files in the repository.
        """
        contents = self.repo.get_contents('')
        file_list = []

        while contents:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                file_data = self.repo.get_contents(file_content.path)
                file_list.append(File(path=file_content.path, content=file_data.decoded_content.decode()))

        return file_list

class File:
    path: str
    content: str

    def __init__(self, path: str, content: str) -> None:
        self.path = path
        self.content = content
