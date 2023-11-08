import unittest
from unittest.mock import patch, Mock
from chat_gpt_developer.github.github_repository import GitHubRepository, File, files_from_json

class TestGitHubRepository(unittest.TestCase):

    @patch('chat_gpt_developer.github.github_repository.Github')
    def setUp(self, mock_github):
        self.mock_repo = Mock()
        self.github_repository = GitHubRepository(
            repository=self.mock_repo,
            mainline_branch='main',
            development_branch='dev',
            token='token'
        )

    def test_files_from_json_valid(self):
        json_str = '[{"path": "path/to/file", "content": "file content"}]'
        files = files_from_json(json_str)
        self.assertEqual(len(files), 1)
        self.assertIsInstance(files[0], File)
        self.assertEqual(files[0].path, 'path/to/file')
        self.assertEqual(files[0].content, 'file content')

    def test_files_from_json_invalid(self):
        json_str = 'invalid json'
        with self.assertRaises(ValueError):
            files_from_json(json_str)

    # More tests...

if __name__ == '__main__':
    unittest.main()
