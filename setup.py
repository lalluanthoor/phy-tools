from setuptools import setup

setup(
    name="phytools",
    version="1.0",
    description="An installer toolkit for installing a bunch of common simulation tools",
    license="MIT",
    author="Lallu Anthoor",
    author_email="lalluanthoor@gmail.com",
    url="https://github.com/lalluanthoor/physics-tools",
    py_modules=[
        "phytools",
        "helper",
        "vasp",
    ],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    phytools=phytools:cli
    """
)
