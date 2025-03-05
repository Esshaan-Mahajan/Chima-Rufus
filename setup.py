from setuptools import setup, find_packages

setup(
    name="Rufus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Esshaan Mahajan",
    description="Rufus: A web crawler for preparing data for RAG systems.",
    url="https://github.com/Esshaan-Mahajan/Chima-Rufus",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
