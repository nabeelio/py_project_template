#
from setuptools import setup

__VERSION__ = '1.0'

requires = (
    'addict==0.4.0',
    'arrow==0.8.0',
    'jinja2==2.8',
    'loadconfig==0.1.1',
    'sortedcontainers==1.5.3',
    'requests==2.10.0',
    'pyyaml==3.11',
)


setup(name='',
    author='Nabeel Shahzad',
    author_email: 'hi@nabs.io',
    version=footbot.__VERSION__,
    url='',
    install_requires=requires,
    test_suite='test'
)
