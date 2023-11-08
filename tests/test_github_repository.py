import json
import pytest
from chat_gpt_developer.github.github_repository import GitHubRepository, File, files_from_json, to_json


class TestGitHubRepository:

    @pytest.fixture
    def repo_instance(self, mocker):
        mocker.patch('github.Github')
        return GitHubRepository(user='testuser', repository_name='testrepo', mainline_branch='main', development_branch=None, token='testtoken')

    def test_files_from_json(self):
        json_str = '[{"path":"test/path.py", "content":"print(\"Hello, World!\")"}]'
        files = files_from_json(json_str)
        assert len(files) == 1
        assert files[0].path == 'test/path.py'
        assert files[0].content == 'print("Hello, World!")'

    def test_to_json(self):
        files = [File(path='test/path.py', content='print("Hello, World!")')]
        json_output = to_json(files)
        expected_json = '[{
    "path": "test/path.py",
    "content": "print(\"Hello, World!\")"
}]'
        assert json.loads(json_output) == json.loads(expected_json)

    # Add more test methods as needed
