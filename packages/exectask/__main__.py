#!/.../python3
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

from exectask.actions import *
from exectask.context import *
from exectask.merge import *
from exectask.printer import *

import argparse
import importlib
import json
import os
import os.path
import sys
import traceback
import types

#
# Main function
#
def main():
	
	# Parse arguments
	def argparse_directory(path):
		if not os.path.exists(path):
			msg = '\'{}\' directory does not exist'.format(path)
			raise argparse.ArgumentTypeError(msg)
		if not os.path.isdir(path):
			msg = '\'{}\' is not a directory'.format(path)
			raise argparse.ArgumentTypeError(msg)
			
		if os.path.isabs(path):
			return path
		return os.path.abspath(path)
	
	parser = argparse.ArgumentParser(
		description='Executes tasks in a coordinated manner.'
	)
	parser.add_argument(
		'taskfile',
		type=argparse.FileType('r'),
		nargs='+',
		help='file containing a task definition'
	)
	parser.add_argument(
		'-a',
		metavar='actionsdir',
		type=argparse_directory,
		nargs='+',
		required=False,
		default=[],
		dest='actionsdir',
		help='action modules directory'
	)
	parser.add_argument(
		'-s',
		metavar='settingsfile',
		type=argparse.FileType('r'),
		nargs='+',
		required=False,
		default=[],
		dest='settingsfile',
		help='file with settings'
	)
	parser.add_argument(
		'-v',
		required=False,
		action='store_true',
		default=False,
		dest='verbose',
		help='verbose output'
	)
	parser.add_argument(
		'-e',
		required=False,
		action='store_true',
		default=False,
		dest='exceptions',
		help='show exceptions stack trace'
	)
	args = parser.parse_args(sys.argv)
	
	# Create printer factory
	if args.verbose:
		printer_fact_level = 1
	else:
		printer_fact_level = 0
	printer_fact = PrinterFactory(printer_fact_level)
	
	# Create action catalog
	actions = {}
	catalog = ActionCatalog(actions, printer_fact)
	for actionsdir in args.actionsdir:
		for fname in os.listdir(actionsdir):
			path = '{}/{}'.format(actionsdir, fname)
			if os.path.isfile(path) and fname.endswith('.py'):
				name = 'exectask.modules.{}'.format(fname[0:len(fname)-3])
				action_catalog_load(catalog, printer_fact, name, path)
				
	# Gather top level variables
	variables = {}
	for settingsfile in args.settingsfile:
		try:
			merge_dict(variables, json.loads(settingsfile.read()))
		except:
			printer = printer_fact.printer(sys.stderr)
			msg = 'Warning: Could not read settings from'
			msg = '{} file \'{}\''.format(msg, settingsfile.name)
			printer.print(msg, 0, 'yellow')
	
	# Execute tasks
	if len(args.taskfile) > 1:
		context = ExecuteTaskContext(actions, printer_fact)
		for taskfile in args.taskfile[1:len(args.taskfile)]:
			try:
				task = json.loads(taskfile.read())
			except:
				task = None
				printer = printer_fact.printer(sys.stderr)
				msg = 'Warning: Could not read task from'
				msg = '{} file \'{}\''.format(msg, taskfile.name)
				printer.print(msg, 0, 'yellow')
				
			if task is not None:
				try:
					# Define built-in variable 'basedir'
					dirname = os.path.dirname(taskfile.name)
					basedir = '\'{}\''.format(os.path.abspath(dirname))
					variables['basedir'] = basedir
					# Execute task
					context.execute_task(task, variables)
				except BaseException as err:
					printer = printer_fact.printer(sys.stderr)
					msg = 'Error: There was a problem executing task'
					msg = '{} from file \'{}\''.format(msg, taskfile.name)
					msg = '{}\nCause: {}'.format(msg, err)
					if args.exceptions:
						msg = '{}:\n{}'.format(msg, traceback.format_exc())
					printer.print(msg, 0, 'red', 'bright')
					
	# Tasks was already executed
	return 0

