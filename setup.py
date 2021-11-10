from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="anonypy",
    version="0.1.7",
    packages=find_packages(),
    author="glassonion1",
    author_email="glassonion999@gmail.com",
    url="https://github.com/glassonion1/anonypy",
    description="Anonymization library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="k-anonymity l-diversity t-closeness mondrian",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
