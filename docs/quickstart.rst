==========
Quickstart
==========

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
