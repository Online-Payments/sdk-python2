import os
import unittest

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def test_collector():
    """Function to collect tests cases to run for the 'pip onlinepayments-sdk-python2 tests' command"""
    from tests import run_unit_tests
    loader = unittest.TestLoader()
    return loader.discover(start_dir=run_unit_tests.__file__)


setup(
    name="onlinepayments-sdk-python2",
    version="4.23.0",
    author="Online Payments support team",
    author_email="96182451+online-payments-support-team@users.noreply.github.com",
    description="SDK to communicate with the Online Payments platform using the Online Payments Server API",
    license="MIT",
    platforms="python 2.7",
    keywords="Online Payments SDK",
    url="https://github.com/Online-Payments/sdk-python2",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],  # Exclude tests
        include="onlinepayments.*"),  # finds all source packages, recursively
    # list non-code files used by the SDK
    package_data={".": ["MANIFEST.in", "README.md", "setup.py", "LICENSE.txt"]},
    # installs all files listed in the MANIFEST.in into the installation (currently does not seem to happen either way)
    include_package_data=True,
    # The pypi homepage is based on the long description, standard interpretation is reStructuredText
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License"
    ],
    scripts=[],  # executable python scripts, none since this is a library
    install_requires=[
        "requests >= 2.20.0",
        "requests-toolbelt >= 0.8.0"
    ]
)
