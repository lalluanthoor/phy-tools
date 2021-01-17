from setuptools import setup

setup(
    name="Physics Tools",
    version="1.0",
    py_modules=["install"],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    ptools=install:cli
    """
)
