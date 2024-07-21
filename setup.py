# from setuptools import setup
# setup(name='pengbot-counter', packages=['src'])

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pengbot-counter",
    version="0.0.5",  
    author="Carlos Arteta",
    author_email="arteta.carlos@gmail.com",
    description="CLI interface for penguin counting (``Counting in the wild''. Arteta et. al. ECCV 2016)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CarlosArteta/pengbot-counter",  
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': [
            'count = pengbot_counter.bin.count:main',
        ],
    },
)