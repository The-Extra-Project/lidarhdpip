from setuptools import find_packages, setup



setup(
    name="bacalau",
    version= "0.1.0",
    description="package for scheduling bacalau jobs and getting the result",
    url="https://github.com/author_name/project_urlname/",
    long_description_content_type="text/markdown",
    author="author_name",
    packages=find_packages(exclude=["tests", ".github"]),
    entry_points={
        "console_scripts": ["project_name = project_name.__main__:main"]
    },
)