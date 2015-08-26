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

import importlib
import importlib.machinery
import inspect
import os
import os.path
import sys
import traceback

class ActionCatalog:
	
	def __init__(self, actions, printer_fact):
		self.__actions = actions
		self.__printer_fact = printer_fact
		
	def add_action(self, name, function):
		try:
			if len(inspect.signature(function).parameters) != 2:
				raise TypeError('Bad parameters')
			self.__actions[name] = function
		except:
			printer = self.__printer_fact.printer(sys.stderr)
			msg = 'Warning: Could not add \'{}\' action:\n'.format(name)
			msg = '{}{}'.format(msg, traceback.format_exc())
			printer.print(msg, 0, 'yellow')
			
def action_catalog_load(catalog, printer_fact, name, path):
	try:
		loader = importlib.machinery.SourceFileLoader(name, path)
		module = loader.load_module()
		module.exectask_actions_load(catalog)
	except:
		printer = printer_fact.printer(sys.stderr)
		msg = 'Warning: Could not add actions from \'{}\':\n'.format(path)
		msg = '{}{}'.format(msg, traceback.format_exc())
		printer.print(msg, 0, 'yellow')

