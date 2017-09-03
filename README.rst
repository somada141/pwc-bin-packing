===============
pwc-bin-packing
===============

Simple bin-packing solver for the PwC interview process.

The problem definition is as follows:

    For a given collection of container sizes and a required load, write an algorithm
    (simple console app will suffice), that will select sufficient containers for
    the load, such that:

    1. the overcapacity is minimized, and
    2. the smallest number of containers are used

The problem resembles a mixture of the bin-packing_ and subset-sum_ problems but as the possibly conflicting objectives haven't been prioritized, several solvers to the above problem prioritizing the different objectives differently were written.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Features
--------

* Command-line interface implemented via click_.
* Length-first solver focusing on finding the shortest bin-combination.
* Capacity-first solver focusing on finding the minimum-capacity bin-combination.
* Solver combining the two objectives.

Usage
-----

This package can be used either via the command-line and the `pbp` script or as importable Python package.

Command-Line Interface
^^^^^^^^^^^^^^^^^^^^^^

Upon successful installation of the package the `pbp` command is made available under the Python environment in which it was installed.

The script can be invoked as such::

    >>> pbp

while appending ``--help`` to the invocation shows the scripts help message as such::

    >>> pbp --help
    Usage: pbp [OPTIONS] LOAD BINS...
    Options:
      --solver-type [length|capacity|combo|all]
      --help                          Show this message and exit.

The different solvers can be invoked via the ``--solver-type`` optional argument which defaults to ``all`` and will provide solutions to the defined problem using each of the solvers::

    >>> pbp 6 2 3 5
    Applying 'length' solver to a load of 6 and the following bins: (2, 3, 5)
    Solution: [(3, 3)]
    Applying 'capacity' solver to a load of 6 and the following bins: (2, 3, 5)
    Solution: [(3, 3)]
    Applying 'combo' solver to a load of 6 and the following bins: (2, 3, 5)
    Solution: [(3, 3)]

In the above example the code was invoked with a load of ``6`` while the available bins were set to a set of ``[2, 3, 5]``.

Example of invoking the length-first solver::

    >>> pbp 6 2 3 5 --solver-type=length
    Applying 'length' solver to a load of 6 and the following bins: (2, 3, 5)
    Solution: [(3, 3)]

Example of invoking the capacity-first solver::

    >>> pbp 9 2 3 5 --solver-type=capacity
    Applying 'capacity' solver to a load of 9 and the following bins: (2, 3, 5)
    Solution: [(2, 2, 5), (3, 3, 3)]

Python Package
^^^^^^^^^^^^^^

Upon successful installation of the package the `pbp` package is also available for direct import::

    >>> import pbp

Solvers can either be instantiated explicitly as such::

    >>> solver_length = pbp.solvers.SolverLengthFirst(load=9, bins=[2, 3, 5])
    >>> solver_capacity = pbp.solvers.SolverCapacityFirst(load=9, bins=[2, 3, 5])
    >>> solver_combo = pbp.solvers.SolverCombo(load=9, bins=[2, 3, 5])

or through the `create_solver` function under the `solvers` module which can automatically create the appropriate solver for a given ``solver_type`` by examining the solver base-class meta-registry as such::

    >>> solver_length = pbp.solvers.create_solver(load=9, bins=[2, 3, 5], solver_type="length")
    >>> solver_capacity = pbp.solvers.create_solver(load=9, bins=[2, 3, 5], solver_type="capacity")
    >>> solver_combo = pbp.solvers.create_solver(load=9, bins=[2, 3, 5], solver_type="combo")

Regardless of the instantiation approach all solvers implement a common interface and provide their solution through their ``solve`` method returning a list of tuples, each of which is a combination of bins for the defined load considered optimal by the given solver as such::

    >>> solver_length.solve()
    [(5, 5)]
    >>> solver_capacity.solve()
    [(2, 2, 5), (3, 3, 3)]
    >>> solver_combo.solve()
    [(2, 2, 5), (3, 3, 3)]

Development
-----------

Setup
^^^^^

This project is entirely developed within a local Vagrant_ VM based on the official ubuntu/trusty64_ base image.

The VM can be spun up through::

    >>> vagrant up

Unit-tests
^^^^^^^^^^

Unit-tests for the application have been written under the `tests` subpackage.

These can be executed via the included `Makefile` as such::

    >>> make test

while unit-testing and coverage can be inspected with::

    >>> make coverage

Documentation
^^^^^^^^^^^^^

The codebase adheres closely to the Google Python Style Guide (https://google.github.io/styleguide/pyguide.html) which is applied to the code comments and docstrings.

The project documentation is generated automatically via Sphinx_ using the napoleon_  extension which can parse Google-style docstrings and improve their legibility prior to rendering.

Documentation can be built via the included Makefile as such::

    >>> make docs


.. _bin-packing: https://en.wikipedia.org/wiki/Bin_packing_problem
.. _subset-sum: https://en.wikipedia.org/wiki/Subset_sum_problem
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _click: http://click.pocoo.org/6/
.. _Vagrant: https://www.vagrantup.com/
.. _ubuntu/trusty64: https://app.vagrantup.com/ubuntu/boxes/trusty64
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _napoleon: https://pypi.python.org/pypi/sphinxcontrib-napoleon
