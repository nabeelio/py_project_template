#
from setuptools import setup


requires = (
    'addict==0.4.0',
    'arrow==0.8.0',
    'bumpversion==0.5.3',
    'jinja2==2.8',
    'loadconfig==0.1.1',
    'sortedcontainers==1.5.3',
    'requests==2.10.0',
    'pytest==2.9.2',
    'pyyaml==3.11',
    'requests==2.10.0',
)

from {{ cookiecutter.package_name }} import \
    __author__,
    __version__

setup(name="{{ cookiecutter.package_name }}",
      version="{{ cookiecutter.package_version }}",
      url="{{ cookiecutter.package_url }}",
      author="{{ cookiecutter.author_name }}",
      author_email="{{ cookiecutter.author_email }}",
      install_requires=requires,
      test_suite='test',
      entry_points={
        'console_scripts': [
            '{{ cookiecutter.package_name }} = {{ cookiecutter.package_name }}.app:main',
        ]
      }
)
