import re
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="trial-version",
    version="1.0",
    description="A trial version of an app.",
    long_description=
"""
This is a trial version""",
    author="Martin Mogusu",
    author_email="martinmogusu@gmail.com",
    url="https://github.com/martinmogusu/trial-version",
    download_url="https://github.com/martinmogusu/trial-version.git",
    license="MIT License",
    packages=[
        "trial_version",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.11",
        "python-decouple",
        "requests"
    ],
    tests_require=[
        "nose",
        "coverage",
    ],
    zip_safe=False,
    test_suite="tests.runtests.start",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)