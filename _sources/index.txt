.. Turk Gate Manager documentation master file, created by
   sphinx-quickstart on Mon Feb  3 17:15:02 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Turk Gate Manager Documentation
===============================

The main function of TurkGateManager is to edit the MySQL database associated with TurkGate to perform the following:

* add requests (worker ids) to a TurkGate group so those workers cannot accept HITs associated with the group in the future

By communicating with the MySQL database and Amazon Mechanical Turk, TurkGateManager also provides the ability to:

* retrieve worker ids from HITs directly via the AWS API
* copy worker ids from an existing group to a new group
* rename groups
* remove worker ids from a group

Using TurkGateManager
---------------------

Download the turkgatemanager package and use in an interactive python session.

Requirements
------------

TurkGateManager requires the following packages:

- `boto <https://github.com/boto/boto>`_
- `sqlalchemy <http://www.sqlalchemy.org/download.html>`_

Documentation
=============

.. toctree::
    :maxdepth: 2

    turkgate-manager
    survey-request
    get-credentials

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

