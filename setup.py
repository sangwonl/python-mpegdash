from os.path import dirname, abspath, join, exists
from setuptools import setup, find_packages

long_description = None
if exists("README.md"):
    long_description = open("README.md").read()

install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(name="mpd_parser",
      packages=["mpd"],
      description="MPEG-DASH MPD(Media Presentation Description) Parser",
      long_description=long_description,
      author='supercast-tv',
      author_email='gamzabaw@gmail.com',
      version="0.1",
      license='MIT',
      zip_safe=False,
      include_package_data=True,
      install_requires=install_reqs,
      url="https://github.com/caststack/python-mpd-parser",
      test_suite='tests.my_module_suite',
     )
