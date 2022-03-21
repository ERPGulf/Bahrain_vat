from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in bahrain_vat/__init__.py
from bahrain_vat import __version__ as version

setup(
	name='bahrain_vat',
	version=version,
	description='BAHRAIN VAT Management and Reporting',
	author='ERPGulf',
	author_email='support@erpgulf.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
