.. bun documentation master file, created by
   sphinx-quickstart on Wed Sep 20 19:58:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================
Welcome to bun!
========================

Backup Now for gentoo
--------------------------------------

``bun`` is a simple backup program built on top of GNU tar and
`invoke <http://www.pyinvoke.org/>`_ tasks.

The philosophy is to:

+ delegate the actual backup to GNU tar and (e.g.) sha256sum
+ very configurable in `yaml <http://www.yaml.org/>`_
+ wraps individual operations with `invoke <http://www.pyinvoke.org/>`_ tasks
+ integrates with `oam <https://github.com/lmiphay/oam>`_
+ installable via emerge/layman

See :doc:`changelog` for changes in this version.

Quickstart
--------------------------------------
* Install the program::

    # layman -L && layman -a lmiphay

  Keyword the program, e.g.::

    app-oam/bun ~amd64

  Then::

    # emerge app-oam/bun

* Review the default settings, make any local changes::

    # vi /etc/bun/bun.yaml

* See what operations a default backup would do::

    # bun pretend

* And then kick off a default backup::

    # bun backup

* Watch the progress of the backup::

    # bun watch

* At some later point verify the checksums of the backup::

    # bun verify --timestamp=20171915-154431

* Restore a backup to a specified location::

    # bun restore --timestamp=20171915-154431 --location=/var/tmp

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
