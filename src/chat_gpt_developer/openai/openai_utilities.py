from src.chat_gpt_developer.openai.openai_chat_gpt import OpenAIChatGPT
from typing import List
from src.chat_gpt_developer.github.github_repository import File
from dataclasses import dataclass


def create_code_solution(issue: 'Issue', client: 'OpenAIChatGPT') -> List[File]:
    # Provide a solution based on the issue
    return []


def summarize_code_solution(issue: 'Issue', files: List[File], client: 'OpenAIChatGPT') -> (str, str):
    # Summarize the code solution
    title = ''
    body = ''
    return title, body
