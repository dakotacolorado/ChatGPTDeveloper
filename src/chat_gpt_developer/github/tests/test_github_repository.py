import unittest
from unittest.mock import MagicMock, patch
from chat_gpt_developer.github.github_repository import GitHubRepository, File


class TestGitHubRepository(unittest.TestCase):

    @patch('chat_gpt_developer.github.github_repository.Github')
    def setUp(self, mock_github):
        self.token = 'test-token'
        self.repo_name = 'test-repo'
        self.mainline_branch = 'main'
        self.development_branch = 'dev'
        self.mock_repo = MagicMock()
        mock_github.return_value.get_repo.return_value = self.mock_repo
        self.git_repo = GitHubRepository(self.token, self.repo_name)

    def test_init(self):
        self.assertEqual(self.git_repo.mainline_branch, 'main')
        self.assertEqual(self.git_repo.development_branch, 'dev')

    @patch('chat_gpt_developer.github.github_repository.GitHubRepository._get_latest_commit')
    @patch('chat_gpt_developer.github.github_repository.GitHubRepository._create_or_get_branch')
    def test_submit_pull_request(self, mock_create_or_get_branch, mock_get_latest_commit):
        mock_get_latest_commit.return_value = 'sha12345'
        self.git_repo.submit_pull_request([], 'Test PR', 'This is a test PR')
        mock_create_or_get_branch.assert_called_once_with(self.mock_repo, self.development_branch, 'sha12345')
        self.mock_repo.create_pull.assert_called_once_with('Test PR', 'This is a test PR', self.development_branch, self.mainline_branch)

if __name__ == '__main__':
    unittest.main()
