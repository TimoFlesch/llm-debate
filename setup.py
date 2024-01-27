from setuptools import setup, find_packages

setup(
    name="llm_debate",
    # py_modules=["llm_debate"],
    version="0.0.1",
    description="A package for letting LLMs debate each other",
    author="Timo Flesch",
    author_email="timo.flesch@googlemail.com",
    url="https://github.com/timoflesch/llm_debates",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.7",
        "duckduckgo_search>=4.1.1",
        "gpt4all>=2.1.0",
        "wikipedia>=1.4.0",
    ],
    entry_points="""
        [console_scripts]
        llm_debate=llm_debate.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
