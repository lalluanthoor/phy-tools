from setuptools import setup

setup(
    name="phy-tools",
    version="1.0",
    description="An installer toolkit for installing a bunch of common simulation tools",
    license="MIT",
    author="Lallu Anthoor",
    author_email="lalluanthoor@gmail.com",
    url="https://github.com/lalluanthoor/physics-tools",
    py_modules=["phy-tools"],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    phy-tools=phy-tools:cli
    """
)
