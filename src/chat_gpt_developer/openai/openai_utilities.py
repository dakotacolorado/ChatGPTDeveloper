import openai
from typing import List
from .github.github_repository import Issue


class OpenAIUtilities:
    def __init__(self, api_key: str, system_prefix: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.system_prefix = system_prefix

    def create_code_solution(self, issue: Issue) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": self.system_prefix},
                {"role": "user", "content": str(issue)}
            ]
        )
        return response.choices[0].message.content

    def summarize_code_solution(self, files: List[File]) -> str:
        file_content = '\n'.join([f'# Filepath: {file.path}\n{file.content}' for file in files])
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Generate a summary for the provided code changes."},
                {"role": "user", "content": file_content}
            ]
        )
        return response.choices[0].message.content