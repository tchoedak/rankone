from setuptools import setup, find_packages

import rankone
pkgs = ['rankone.%s' %s for s in find_packages('./rankone')]
pkgs.append('rankone')


with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='rankone',
    version='0.0.1',
    packages=pkgs,
    description='',
    author='tchoedak@gmail.com',
    install_requires=requirements,
    tests_require=['pytest'],
    test_suite="tests",
)