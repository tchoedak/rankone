import pathlib
from setuptools import setup, find_packages


pkgs = ['rankone.%s' % s for s in find_packages('./rankone')]
pkgs.append('rankone')

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='rankone',
    version='0.0.4',
    packages=pkgs,
    description='RankOne is a discord bot that manages a Elo ladder for pickup games.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='tchoedak@gmail.com',
    install_requires=requirements,
    entry_points={'console_scripts': ['rankone=rankone.client:start']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="test",
)
