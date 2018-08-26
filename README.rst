CGNS Python Interface
=====================

.. image:: https://travis-ci.org/chiao45/cgns_wrapper.svg?branch=master
    :target: https://travis-ci.org/chiao45/cgns_wrapper
.. image:: https://img.shields.io/pypi/v/cgns_wrapper.svg?branch=master
    :target: https://pypi.org/project/cgns-wrapper/

Introduction
------------

CGNS Wrapper (`cgns_wrapper`) provides you a Python interface for
`CFD General Notation System <https://cgns.github.io/>`_ (`CGNS`), one of the
popular CFD data representations.

`cgns_wrapper` is a **module** wrapper of
`pyCGNS <https://github.com/pyCGNS/pyCGNS>`_. Particularly speaking,
`cgns_wrapper` wraps
`pyCGNS.MAP <http://pycgns.sourceforge.net/MAP/_index.html>`_ as
``cgns_wrapper.io`` and
`pyCGNS.PAT.cgnslib <http://pycgns.sourceforge.net/PAT/_index.html>`_ as
``cgns_wrapper.cgnslib``.

Then core motivation of this project is to glue `CGNS` and PyPI, so that people
can easily install it through pip.

**NOTE** If you already have manually configured and installed `pyCGNS`,
then this package has no benefits.

**NOTE** This package doesn't require you install `CGNS`, but having it is
still useful and, in most cases, necessary.

Documentation
-------------

Please refer to original `CGNS` and `pyCGNS` documentation.

Installation
------------

.. code-block:: console

  $ pip install cgns_wrapper --user

License
-------

MIT License

Copyright (c) 2018 Qiao Chen
