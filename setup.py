# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in clinical_study_questionnaire/__init__.py
from clinical_study_questionnaire import __version__ as version

setup(
	name='clinical_study_questionnaire',
	version=version,
	description='Apps for Questionnaire for clinical Study. ',
	author='Hemolife',
	author_email='hemolifeservice@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
