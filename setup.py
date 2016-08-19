#
from setuptools import setup


requires = (
    'addict==0.4.0',
    'arrow==0.8.0',
    'jinja2==2.8',
    'loadconfig==0.1.1',
    'sortedcontainers==1.5.3',
    'requests==2.10.0',
    'pytest==2.9.2',
    'pyyaml==3.11',
    'requests==2.10.0',
)

from app import \
    __APP_NAME__, \
    __AUTHOR__, \
    __AUTHOR_EMAIL__, \
    __PROJECT_URL__, \
    __VERSION__

setup(name=__APP_NAME__,
      author=__AUTHOR__,
      author_email=__AUTHOR_EMAIL__,
      version=__VERSION__,
      url=__PROJECT_URL__,
      install_requires=requires,
      test_suite='test',
      entry_points={
        'console_scripts': [
            '{app} = {app}.app:main'.format(app=__APP_NAME__),
        ]
      }
)
