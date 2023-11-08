from dataclasses import dataclass
from typing import List, Optional
from github import Github, Repository
from github.GithubException import GithubException
from github.InputGitTreeElement import InputGitTreeElement
import json


def parse_json_to_files(json_str: str) -> List['File']:
    return [
        File(**file) for file in json.loads(json_str)
    ]


class GitHubRepository:
    def __init__(self, token: str, repository_name: str, mainline_branch='main', development_branch='dev'):
        self.gh = Github(token)
        self.repo: Repository = self.gh.get_repo(repository_name)
        self.mainline_branch = mainline_branch
        self.development_branch = development_branch

    @staticmethod
    def _get_latest_commit(repo: Repository, branch: str) -> str:
        return repo.get_branch(branch).commit.sha

    @staticmethod
    def _create_or_get_branch(repo: Repository, branch_name: str, sha: str) -> None:
        ref = f'heads/{branch_name}'
        try:
            repo.get_git_ref(ref)
        except GithubException:
            repo.create_git_ref(f'refs/{ref}', sha)

    def submit_pull_request(self, files: List['File'], title: str, body: str) -> None:
        mainline_sha = self._get_latest_commit(self.repo, self.mainline_branch)
        self._create_or_get_branch(self.repo, self.development_branch, mainline_sha)

        base_tree = self.repo.get_git_tree(mainline_sha)
        element_list = [InputGitTreeElement(file.path, '100644', 'blob', content=file.content) for file in files]
        tree = self.repo.create_git_tree(element_list, base_tree)

        commit = self.repo.create_git_commit(title, tree, [mainline_sha])
        self.repo.get_git_ref(f'heads/{self.development_branch}').edit(commit.sha)

        self.repo.create_pull(title, body, self.development_branch, self.mainline_branch)

    def get_repo_contents(self, path: str = '') -> List['File']:
        contents = self.repo.get_contents(path)
        file_list = []

        while contents:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                file_data = self.repo.get_contents(file_content.path)
                file_list.append(File(path=file_content.path, content=file_data.decoded_content.decode()))

        return file_list


@dataclass(frozen=True)
class File:
    path: str
    content: str


@dataclass(frozen=True)
class Issue:
    title: str
    body: str
    criteria: str