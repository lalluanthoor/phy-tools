from setuptools import setup, find_packages
from codecs import open

with open("README.md", "r", "utf-8") as readme:
    README = readme.read()

setup(
    name="phytools",
    version="0.1.0",
    description="An installer toolkit for installing a bunch of common simulation tools",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Lallu Anthoor",
    author_email="lalluanthoor@gmail.com",
    url="https://github.com/lalluanthoor/physics-tools",
    packages=find_packages(),
    package_data={"": ["LICENSE", "README.md"]},
    include_package_data=True,
    python_requires=">=3.5",
    platforms=["Linux"],
    install_requires=[
        "Click>=7.1.2",
        "requests>=2.25.1",
    ],
    entry_points="""
    [console_scripts]
    phytools=phytools.phytools:cli
    """,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
