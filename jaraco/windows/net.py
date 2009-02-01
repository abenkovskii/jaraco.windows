#!/usr/bin/env python

# $Id$

"""
API hooks for network stuff.
"""

__all__ = ('AddConnection')

import ctypes
import ctypes.wintypes

from jaraco.windows.util import ensure_unicode
from jaraco.windows.error import WindowsError

# MPR - Multiple Provider Router
mpr = ctypes.windll.mpr

RESOURCETYPE_ANY = 0

class NETRESOURCE(ctypes.Structure):
	_fields_ = [
		('scope', ctypes.wintypes.DWORD),
		('type', ctypes.wintypes.DWORD),
		('display_type', ctypes.wintypes.DWORD),
		('usage', ctypes.wintypes.DWORD),
		('local_name', ctypes.wintypes.LPWSTR),
		('remote_name', ctypes.wintypes.LPWSTR),
		('comment', ctypes.wintypes.LPWSTR),
		('provider', ctypes.wintypes.LPWSTR),
		]

def AddConnection(
	remote_name,
	type=RESOURCETYPE_ANY,
	local_name=None,
	provider_name=None,
	user=None,
	password=None,
	flags=0):
	user, password = map(ensure_unicode, (user, password))
	resource = NETRESOURCE(
		type=type,
		remote_name=remote_name,
		local_name=local_name,
		provider_name=provider_name,
		# WNetAddConnection2 ignores the other members of NETRESOURCE
		)
	
	result = mpr.WNetAddConnection2W(
		ctypes.byref(resource),
		password,
		user,
		flags,
		)

	if result != 0:
		raise WindowsError(result)