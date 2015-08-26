#
# This file is part of EXECTASK.
#
# EXECTASK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EXECTASK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EXECTASK.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

setup(
	name='exectask',
	version='0.1.0',
	
	author='Miquel A. Ferran Gonzalez',
	author_email='miquel.ferran.gonzalez@gmail.com',
	
	packages=find_packages('packages'),
	package_dir={
		'': 'packages'
	},
	extras_require={
		'color': [
			'colorama>=0.3.3'
		]
	},
	entry_points={
		'console_scripts': [
			'exectask=exectask.__main__:main'
		]
	},
	url='http://pypi.python.org/pypi/exectask_0.1.0/',
	
	license='LICENSE.txt',
	description='Executes tasks in a coordinated manner.',
	long_description=open('README.md').read()
)

