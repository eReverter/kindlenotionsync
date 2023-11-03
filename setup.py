#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

setup(
    name="kindlenotionsync",
    version="1.0.0",
    author="Enric Reverter",
    author_email="ereverter.ds@gmail.com",
    description="Export data from <Notes and Highlights> Kindle htmls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eReverter/kindlenotionsync",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "kindlenotionsync = kindlenotionsync.__main__:main",
        ],
    },
)
