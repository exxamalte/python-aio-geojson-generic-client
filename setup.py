import os

from setuptools import find_packages, setup

NAME = "aio_geojson_generic_client"
AUTHOR = "Malte Franken"
AUTHOR_EMAIL = "coding@subspace.de"
DESCRIPTION = "An generic async GeoJSON client library."
URL = "https://github.com/exxamalte/python-aio-geojson-generic-client"

REQUIRES = [
    "aio_geojson_client>=0.17",
    "aiohttp>=3.7.4,<4",
    "pytz>=2019.01",
]


with open("README.md", "r") as fh:
    long_description = fh.read()

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = {}
with open(os.path.join(HERE, NAME, "__version__.py")) as f:
    exec(f.read(), VERSION)  # pylint: disable=exec-used

setup(
    name=NAME,
    version=VERSION["__version__"],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests", "tests.*")),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES,
)
