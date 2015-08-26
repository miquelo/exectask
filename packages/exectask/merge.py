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

def merge_literal(obj):
	try:
		return obj.literal()
	except:
		return obj
		
def merge_obj(obj, other):
	if isinstance(obj, list):
		merge_list(obj, other)
	if isinstance(obj, dict):
		merge_dict(obj, other)
		
def merge_list(obj, other):
	obj.extend(merge_literal(other))
	
def merge_dict(obj, other):
	for key, value in merge_literal(other).items():
		try:
			merge_obj(obj[key], value)
		except:
			obj[key] = value

