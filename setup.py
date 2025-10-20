from setuptools import setup, find_packages

setup(
    name="us_visa",
    version="0.0.1",
    author="Omar Rashid",
    author_email="omarrashid852@gmail.com",
    packages=find_packages(include=["us_visa", "us_visa.*"]),  # only include your main package
    install_requires=[],
)
