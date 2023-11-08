import pytest
from unittest.mock import MagicMock
from chat_gpt_developer.github.github_repository import files_from_json, File, GitHubRepository


class TestGitHubRepository:
    @staticmethod
    def test_files_from_json_valid():
        json_str = '[{"path": "test/path", "content": "some content"}]'
        files = files_from_json(json_str)
        assert files == [{'path': 'test/path', 'content': 'some content'}]

    @staticmethod
    def test_files_from_json_invalid():
        with pytest.raises(ValueError):
            files_from_json('this is not a valid json string')

    @pytest.fixture
    def mock_github_repository(self) -> GitHubRepository:
        repository = GitHubRepository(
            user='user',
            repository_name='repo',
            mainline_branch='main',
            development_branch='dev',
            token='token'
        )
        repository.github = MagicMock()
        repository.repo = MagicMock()
        return repository

    # More tests would be added here following best practices
