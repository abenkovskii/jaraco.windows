.. image:: https://img.shields.io/pypi/v/jaraco.windows.svg
   :target: https://pypi.org/project/jaraco.windows

.. image:: https://img.shields.io/pypi/pyversions/jaraco.windows.svg

.. image:: https://img.shields.io/pypi/dm/jaraco.windows.svg

.. image:: https://img.shields.io/travis/jaraco/jaraco.windows/master.svg
   :target: http://travis-ci.org/jaraco/jaraco.windows

.. contents::

Status and License
------------------

``jaraco.windows`` aims to provide a pure-python interface to Windows
APIs using ctypes. This package is not designed to be exhaustive, but
rather to supply interfaces as they are needed by the contributors.

``jaraco.windows`` is written by Jason R. Coombs.  It is licensed under an
`MIT-style permissive license
<http://www.opensource.org/licenses/mit-license.php>`_.

Package Contents
----------------

``jaraco.windows`` contains several modules for different purposes. For now,
read the source. Eventually, I hope to put high-level descriptions of the modules
here.

Installation
------------

You should install this module the normal way using pip or easy_install.

If you want to monkeypatch the os module to include symlink compatibility, you
should add the following to your ``usercustomize`` or ``sitecustomize`` module:

	``import jaraco.windows.filesystem as fs; fs.patch_os_module()``

Thereafter, you should be able to use ``os.symlink`` and ``os.readlink`` in Windows
Vista and later using the same interface as on Unix.

Note that ``jaraco.windows.filesystem.symlink`` takes an additional optional
parameter ``target_is_directory``, which must be specified if the target is not
present and is expected to be a directory once present.

Contribute
----------

If jaraco.windows doesn't supply the interface you require for your
application, consider creating the interface and providing a patch
to the author.
