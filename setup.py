from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erplite/__init__.py
from erplite import __version__ as version

setup(
	name="erplite",
	version=version,
	description="ERPLite for Changemakers",
	author="T4G Labs",
	author_email="sherin@efeone.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
