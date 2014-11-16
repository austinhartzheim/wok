#! /usr/bin/env python3
from distutils.core import setup


setup(
    name='Wok',
    author='Austin Hartzheim',

    version='1.2.1',
    packages=['wok'],
    license='GNU GPL v3',
    description='Download menus from UW-Madison\'s NetNutrition website.',
    long_description=open('README.md').read(),
    url='austinhartzheim.me/projects/wok/'
)
