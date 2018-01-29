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

See :doc:`quickstart` for a quick install and trial drive.

See :doc:`changelog` for changes in this version.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   config
   verify
   api
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
