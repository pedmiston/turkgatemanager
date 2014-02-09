TurkGate Manager Documentation
===============================

TurkGate
--------

If you use Amazon Mechanical Turk to recruit participants for various data collection tasks, you might find yourself in a situation where you'd like to prevent mTurk workers who have already participated in a HIT "A" from participating in a new HIT "B". If you have access to a server, TurkGate is a great solution. 

TurkGate (\ **g**\ rouping and **a**\ ccess **t**\ ools for **e**\ xternal surveys for use with Amazon Mechanical **Turk**) is a web application developed by Adam Darlow and Gideon Goldin. 

* `TurkGate main page <http://gideongoldin.github.io/TurkGate/>`_
* `TurkGate wiki <https://github.com/gideongoldin/TurkGate/wiki>`_

TurkGateManager
----------------

TurkGate\ *Manager* is a python class that serves as an addendum to TurkGate. The main function of TurkGateManager is to edit the MySQL database used by the TurkGate web application to accomplish the following:

* add requests (worker ids) to a TurkGate group (prevents those workers from accepting a subsequent HIT from the same group)
* retrieve worker ids directly from completed mTurk HITs
* copy worker ids from an existing group to a new group
* rename groups
* remove worker ids from a group

Installation
------------

To "install", download the repository and edit ``credentials.yaml`` with your own credentials (and remove the ``.default`` suffix from the file name). See the `Documentation <http://pedmiston.github.io/turkgatemanager/#documentation>`_ for more.

TurkGateManager requires the following python packages:

* `boto <https://github.com/boto/boto>`_
* `sqlalchemy <http://www.sqlalchemy.org/download.html>`_

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

