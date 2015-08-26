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

from exectask.expression import *
from exectask.merge import *

import json
import sys

class ExecuteTaskContext:
	
	class NonePrinterFactory:
	
		def printer(self, out):
			return NonePrinter()
			
	class NonePrinter:
	
		def print(self, text, level=0, color=None, style=None):
			pass
			
	def __init__(self, actions={}, printer_fact=NonePrinterFactory()):
		self.__actions = actions
		self.__printer_fact = printer_fact
		self.__variables_stack = [
			{}
		]
		self.__variables = ExpressionDict(self.__variables_stack[-1], self)
		
	def __len__(self):
		return self.__variables.__len__()
		
	def __length_hint__(self):
		return self.__variables.__length_hint__()
		
	def __getitem__(self, key):
		return self.__variables.__getitem__(key)
		
	def __missing__(self):
		self.__variables.__missing__()
		
	def __setitem__(self, key, value):
		self.__variables.__setitem__(key, value)
		
	def __delitem__(self, key):
		self.__variables.__delitem__(key)
		
	def __iter__(self):
		return self.__variables.__iter__()
		
	def __reversed__(self):
		return self.__variables.__reversed__()
		
	def __contains__(self, item):
		return self.__variables.__contains__(item)
		
	def items(self):
		return self.__variables.items()
		
	def printer(self, out):
		return self.__printer_fact.printer(out)
		
	def execute_task(self, task, variables={}):
		# Check parameter types
		if not isinstance(task, dict):
			raise TypeError('\'task\' must be a dictionary')
		if not isinstance(variables, dict):
			raise TypeError('\'variables\' must be a dictionary')
		
		# Gather top variables
		top_vars = self.__variables_stack[-1]
		try:
			task_vars = task['variables']
			if not isinstance(task_vars, dict):
				raise TypeError('Task \'variables\' must be a dictionary')
			merge_dict(top_vars, task_vars)
		except KeyError:
			pass
		merge_dict(top_vars, variables)
		
		# Update variables stack
		self.__variables_stack.append(top_vars)
		self.__variables = ExpressionDict(self.__variables_stack[-1], self)
		
		# Gather description and actions
		task_desc = None
		task_actions = []
		for key, value in task.items():
			if key == 'variables':
				pass # Already gathered
			elif key == 'description':
				if not isinstance(value, str):
					raise TypeError('Task \'description\' must be an string')
				task_desc = expression_eval(value, self)
			elif key == 'actions':
				if not isinstance(value, list):
					raise TypeError('Task \'actions\' must be a list')
				task_actions = value
			else:
				raise TypeError('Unknown task field \'{}\''.format(key))
				
		# Print task information
		printer = self.__printer_fact.printer(sys.stdout)
		if task_desc is not None:
			printer.print('==> {}'.format(task_desc), 0, 'white', 'bright')
		printer.print('Variables:', 1)
		printer.print(json.dumps(top_vars, indent=4, sort_keys=True), 1)
		printer.print('Actions:', 1)
		printer.print(json.dumps(task_actions, indent=4, sort_keys=True), 1)
		
		# Call task actions
		for action in ExpressionList(task_actions, self):
			self.call_action(action)
			
		# Restore variables stack
		self.__variables_stack.pop()
		self.__variables = ExpressionDict(self.__variables_stack[-1], self)
		
	def call_action(self, action):
		# Check parameter types
		if not isinstance(action, dict):
			raise TypeError('\'action\' must be a dictionary')
			
		# Gather name and parameters
		name = None
		parameters = {}
		for key, value in action.items():
			if key == 'name':
				if not isinstance(value, str):
					raise TypeError('Action \'name\' must be an string')
				name = value
			elif key == 'parameters':
				if not isinstance(value, dict):
					raise TypeError('Action \'parameters\' must be a '
							'dictionary')
				parameters = value
			else:
				raise TypeError('Unknown action field \'{}\''.format(key))
				
		if name is None:
			raise TypeError('Action \'name\' must be defined')
			
		# Call action function
		try:
			fn = self.__actions[name]
		except KeyError:
			raise TypeError('Action \'{}\' was not found'.format(name))
		action_locals = {
			'fn': fn,
			'context': self,
			'parameters': parameters
		}
		eval('fn(context, parameters)', {}, action_locals)

