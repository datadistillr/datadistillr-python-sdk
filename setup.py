#!/usr/bin/env python
from setuptools import setup, find_packages

"""
   Copyright 2021 DataDistillr Inc.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       https://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

setup_args = dict(
    name='datadistillr',
    version='0.1.2',
    author='Charles Givre',
    author_email='charles@datadistillr.com',
    packages=find_packages(include=['datadistillr', 'datadistillr.*']),
    url='https://github.com/datadistillr/datadistillr-python-sdk',
    license="Apache",
    description='A Python SDK for interacting with datasets created on DataDistillr',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas",
        "requests"
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: SQL',
        'Operating System :: OS Independent',
        'Topic :: Database'
    ]
)


def main():
    setup(**setup_args)


if __name__ == '__main__':
    main()
