Setup
=====

Padmini's main code does not depend on external libraries. It does depend on
some side data, which is included with the project.


Data Files
----------

All necessary data files are included in the ``data/`` directory. Currently,
the only file in ``data/`` is:

- ``dhatupatha.tsv``, an accented Dhatupatha created from various sources. This
  file is mostly consistent with the Dhatupatha used by
  https://ashtadhyayi.com.


Dependencies
------------

Padmini's main code has no external dependencies. 

Test and development dependencies are in ``requirements-dev.txt``. You can
install these requirements with:

    pip install -r requirements-dev.txt

The main requirements here are:

- ``black`` for code formatting
- ``sphinx`` for documentation
- ``py.test`` for unit tests

You can run all of these commands through ``make``. For example, running ``make
lint`` in the project directory will apply code formatting to the entire
project. See ``Makefile`` for details.
