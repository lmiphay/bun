======
Verify
======

* To verify the checksums of a specified backup::

    # bun verify --timestamp=20171915-154431
    /backup/20180129-093137/homes.tar.xz -: OK
    /backup/20180129-093137/bun.tar.xz -: OK
    #

* If checksum fails OK will be replaced with FAILED,
  and the program will exit with a return code of 1
  (otherwise it will exit with 0)::

    # bun verify --timestamp=20171915-154431
    /backup/20180127-103137/homes.tar.xz -: FAILED
    #

* The checked tarballs are based on the currently configured
  specs (not the specs configured at the time the backup was
  made).

* To manually check any particular tarball::

    # cd .../backup/20171915-154431
    # sha256sum -c oam.tar.xz.sha256sum <oam.tar.xz
    -: OK
    #

* The check subcommand can be used to verify all
  tarballs in a specified directory::

    # bun check /local/remote-backup
    /local/remote-backup/homes.tar.xz -: OK
    #
