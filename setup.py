#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click==6.7',
    'wheel==0.29.0',
    'urllib3==1.26.5',
    'pyasn1==0.1.9',
    'pyOpenSSL==16.2.0',
    'ndg-httpsclient==0.4.0',
]

setup_requirements = [
    'tox==2.3.1',
    'coverage==4.1',
    'Sphinx==1.4.8',
    'docutils==0.12',
    'sphinxcontrib-napoleon==0.6.1',
    'pytest==3.1.3',
    'pytest-runner'
]

test_requirements = [
    'pytest==3.1.3',
    'pytest-runner'
]

setup(
    name='pbp',
    version='0.1.0',
    description="Simple bin-packing solver for the PwC interview process.",
    long_description=readme + '\n\n' + history,
    author="Adamos Kyriakou",
    author_email='somada141@gmail.com',
    url='https://github.com/somada141/pbp',
    packages=find_packages(include=['pbp']),
    entry_points={
        'console_scripts': [
            'pbp=pbp.pbp:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pbp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
