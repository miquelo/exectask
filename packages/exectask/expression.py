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

import json

class ExpressionCont:
		
	def resolver(self):
		return self.__resolver
		
	def literal(self):
		return self.__literal
		
class ExpressionList(list):
	
	def __init__(self, original, resolver):
		self.extend(original)
		self.__resolver = resolver
		
	def __getitem__(self, key):
		return expression_infer(super().__getitem__(key), self.__resolver)
		
	def __iter__(self):
		return ExpressionListIterator(super().__iter__(), self.__resolver)
		
	def __reversed__(self):
		return ExpressionListIterator(super().__reversed__(), self.__resolver)
		
	def copy(self):
		return super().copy()
		
class ExpressionListIterator:

	def __init__(self, it, resolver):
		self.__it = it
		self.__resolver = resolver
		
	def __iter__(self):
		return self
		
	def __next__(self):
		return expression_infer(self.__it.__next__(), self.__resolver)
		
class ExpressionDict(dict):

	def __init__(self, original, resolver):
		self.update(original)
		self.__resolver = resolver
		
	def __getitem__(self, key):
		return expression_infer(super().__getitem__(key), self.__resolver)
		
	def __iter__(self):
		return ExpressionDictIterator(super().__iter__(), self.__resolver)
		
	def __reversed__(self):
		return ExpressionDictIterator(super().__reversed__(), self.__resolver)
		
	def items(self):
		return [(key, expression_infer(value, self.__resolver))
				for key, value in super().items()]
				
class ExpressionDictIterator:

	def __init__(self, it, resolver):
		self.__it = it
		self.__resolver = resolver
		
	def __iter__(self):
		return self
		
	def __next__(self):
		return self.__it.__next__()
		
def expression_eval(value, resolver):
	if isinstance(value, str):
		return eval(value, {}, resolver)
	return value
	
def expression_infer(value, resolver):
	if not isinstance(value, ( ExpressionList, ExpressionDict )):
		if isinstance(value, list):
			return ExpressionList(value, resolver)
		if isinstance(value, dict):
			return ExpressionDict(value, resolver)
		if isinstance(value, str):
			return expression_eval(value, resolver)
	return value

