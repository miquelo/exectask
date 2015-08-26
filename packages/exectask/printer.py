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

class PrinterFactory:

	def __init__(self, level):
		try:
			self.__level = level
			self.__colorama = importlib.import_module('colorama')
			self.__colorama.init()
			self.__printer = self.__printer_colorama
		except:
			self.__printer = self.__printer_default
			
	def printer(self, out):
		return self.__printer(out)
		
	def __printer_default(self, out):
		return PrinterDefault(out, self.__level)
		
	def __printer_colorama(self, out):
		return PrinterColorama(out, self.__level, self.__colorama)
		
		
class PrinterBase:

	def __init__(self, out, level):
		self.__out = out
		self.__level = level
		
	def print(self, text, level):
		if level <= self.__level:
			self.__out.write('{}\n'.format(text))

class PrinterDefault(PrinterBase):

	def __init__(self, out, level):
		super().__init__(out, level)
			
	def print(self, text, level=0, color=None, style=None):
		super().print(text, level)
		
class PrinterColorama(PrinterBase):
	
	def __init__(self, out, level, colorama):
		super().__init__(out, level)
		self.__colorama = colorama
		self.__color_codes = {
			'black': self.__colorama.Fore.BLACK,
			'red': self.__colorama.Fore.RED,
			'green': self.__colorama.Fore.GREEN,
			'yellow': self.__colorama.Fore.YELLOW,
			'blue': self.__colorama.Fore.BLUE,
			'magenta': self.__colorama.Fore.MAGENTA,
			'cyan': self.__colorama.Fore.CYAN,
			'white': self.__colorama.Fore.WHITE
		}
		self.__style_codes = {
			'dim': self.__colorama.Style.DIM,
			'normal': self.__colorama.Style.NORMAL,
			'bright': self.__colorama.Style.BRIGHT
		}
		
	def print(self, text, level=0, color=None, style=None):
		tbeg = ''
		tend = ''
		try:
			tbeg = '{}'.format(self.__color_codes[color])
			tend = '{}'.format(self.__colorama.Fore.RESET)
		except:
			pass
		try:
			tbeg = '{}{}'.format(tbeg, self.__style_codes[style])
			tend = '{}{}'.format(self.__colorama.Style.RESET_ALL, tend)
		except:
			pass
		super().print('{}{}{}'.format(tbeg, text, tend), level)

