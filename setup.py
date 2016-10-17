from os.path import dirname, abspath, join, exists
from setuptools import setup

long_description = None
if exists("README.md"):
    long_description = open("README.md").read()

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]
tests_reqs = [req for req in open(abspath(join(dirname(__file__), 'test-requirements.txt')))]

setup(
  name="mpegdash",
  packages=["mpegdash"],
  description="MPEG-DASH MPD(Media Presentation Description) Parser",
  long_description=long_description,
  author="supercast",
  author_email="gamzabaw@gmail.com",
  version="0.1.5",
  license="MIT",
  zip_safe=False,
  include_package_data=True,
  install_requires=install_reqs,
  url="https://github.com/caststack/python-mpegdash",
  tests_require=tests_reqs,
  test_suite="tests.my_module_suite",
  classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],
)
