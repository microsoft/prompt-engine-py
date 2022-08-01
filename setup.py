import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prompt-engine-py",
    version="0.0.2",
    author="Abhishek Masand",
    author_email="amasand@microsoft.com",
    description="This package is a utility library for creating and maintaining prompts for Large Language Models (LLMs).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/prompt-engine-py",
    project_urls={
        "Bug Tracker": "https://github.com/microsoft/prompt-engine-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    package_data={'prompt_engine': ['utils/encoder.json', 'utils/vocab.bpe']},
)