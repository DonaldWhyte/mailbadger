from setuptools import setup
from setuptools import find_packages
import os
import mailbadger

currentFileDirectory = os.path.dirname(__file__)
with open(os.path.join(currentFileDirectory, "README.md"), "r") as f:
    readme = f.read()

print(find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]))

setup(
    name="mailbadger",
    version=mailbadger.VERSION,
    description="TODO",
    long_description=readme,
    author="Donald Whyte",
    author_email="donaldwhyte0@gmail.com",
    url="https://github.com/DonaldWhyte/mailbadger",
    classifiers=[
        "Development Status :: 3 - Alpha Development Status"
        "Intended Audience :: Developers",
        "Programming Language :: Python 3",
        "Programming Language :: Python 3.2",
        "Programming Language :: Python 3.3",
    ],
    keywords="email detector validator mail server smtp script",
    license="MIT",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    scripts=('mailbadger.py',),
    data_files=[ (".", ["LICENSE"]) ],
    test_suite='tests'
)
