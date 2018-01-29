==========
Quickstart
==========

* Install the program::

    # layman -L && layman -a lmiphay

  Keyword the program, e.g.::

    app-oam/bun ~amd64

  Add app-oam as a category (if it is not already)::

    # echo app-oam >>/etc/portage/categories

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

* At some later point verify the checksums of a specified backup::

    # bun verify --timestamp=20171915-154431

* Restore a specific backup to a specified location::

    # bun restore --timestamp=20171915-154431 --location=/var/tmp
