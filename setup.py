#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='makobot',
    description='A Slack bot to monitor for potential security rissks.',
    author='Swimlane LLC',
    author_email='info@swimlane.com',
    url='https://github.com/swimlane/makobot',
    version='0.3.6',
    license='MIT',
    install_requires=['requests', 'slackbot', 'threatconnect'],
    tests_require=['mock', 'nose'],
    test_suite='nose.collector',
    packages=find_packages(exclude=('tests')),
    keywords='slack security bot malware ip url reputation',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
    ]
)
