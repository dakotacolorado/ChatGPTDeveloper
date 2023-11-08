from setuptools import setup, find_packages

setup(
    name="chat_gpt_developer",
    version="0.1",
    author="Dakota James Parker",
    description="A Chat GPT Bot that can write, review, and submit code on GitHub.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
)