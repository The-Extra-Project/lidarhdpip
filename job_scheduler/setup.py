from setuptools import setup
import io
import os

def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content



def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]




setup(
    name="job_scheduler",
    version="0.0.1",
    author="",
    description="Job scheduler of surface reconstruction pipeline running bacalhau jobs",    
    url="",
    packages=['job_scheduler']
    
    
)


