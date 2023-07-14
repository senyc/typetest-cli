================
typetest-cli
================

Python versions
===============

``typetest-cli`` works with all versions of python >= 3.8


Installation
============

pip install
-----------

.. code-block:: python 

    pip install typetest-cli

GitHub
-------


.. code-block:: bash

    git clone https://github.com/senyc/typetest-cli
    cd typetest-cli
    python setup.py install

Running ``typetest-cli``
========================

After install you should be able to run the program with ``typetest`` or ``typetest-cli``

Usage
--------

.. code-block::

    usage: typetest [-h] [--hide-acc] [--hide-wpm] [--only-base] [--no-blocking]
    
    Lightweight typing speed commandline tool. Can be exited with Ctrl-c or return.
    
    options:
      -h, --help         show this help message and exit
      --hide-acc, -a     hides the accuracy statistic
      --hide-wpm, -w     hides the word per minute statistic
      --only-base, -b    Only uses the base text
      --no-blocking, -n  Do not block input after 3 failed attmpts
    
    Will only disply typing speed and accuracy upon completion of the line

