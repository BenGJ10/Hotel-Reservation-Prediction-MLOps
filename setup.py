from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "hotelreservation",
    version = "0.0.1",
    author = "BenGJ",
    author_email = "bengj1015@gmail.com",
    packages = find_packages(),
    instsll_requires = requirements
)