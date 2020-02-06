"""
.. module:: setup.py

   :platform: Unix
   :synopsis: stests setup.

.. moduleauthor:: Casper Labs LLC <dev@casperlabs.io>

"""
import os
import re
from codecs import open

from setuptools import setup
from setuptools import find_packages


# Library name.
NAME = "stests"

# Library 3rd party python dependencies.
REQUIRES = [
    'casperlabs_client',
    'cryptography',
    'dataclasses-json',
    'redis',
    'fakeredis',
    'hiredis',
    'dramatiq',
    'pytest',
    'supervisor',
    'tox'
    ]


def _read(fname):
    """Returns content of a file.

    """
    fpath = os.path.dirname(os.path.realpath(__file__))
    fpath = os.path.join(fpath, fname)
    with open(fpath, mode='r', encoding='utf-8') as file_:
        return file_.read()


setup(
    author='CasperLabs LLC',
    author_email='testing@casperlabs.io',
    cmdclass={},
    description='stests is a python library for running Casper Labs system tests.',
    entry_points={},
    include_package_data=False,
    install_requires=REQUIRES,
    keywords="casperlabs blockchain smart-contracts",
    license='CasperLabs Open Source License (COSL)',
    long_description=_read('README.md'),
    long_description_content_type="text/markdown",
    name=NAME,
    packages=find_packages(),
    project_urls={
        "Source": "https://github.com/CasperLabs/stests/tree/master/stests",
        "Readme": "https://github.com/CasperLabs/stests/blob/master/README.md"
    },
    python_requires=">=3.7.0",
    setup_requires=[],
    url='https://github.com/CasperLabs/stests',
    version="0.1.1",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: CasperLabs Open Source License (COSL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
