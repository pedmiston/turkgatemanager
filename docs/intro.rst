TurkGateManager
===============

The main function of TurkGateManager is to edit the MySQL database associated with TurkGate to perform the following:

* add requests (worker ids) to a TurkGate group so those workers cannot accept HITs associated with the group in the future

By communicating with the MySQL database and Amazon Mechanical Turk, TurkGateManager also provides the ability to:

* retrieve worker ids from HITs directly via the AWS API
* copy worker ids from an existing group to a new group
* rename groups
* remove worker ids from a group

TurkGate terminology
--------------------

A participant taking a survey is associated with a single row in the MySQL database called a *request*. Each *request* has the following attributes:

* *workerID* : a unique identifier for each worker provided by Amazon
* *URL* : the URL of the survey
* *groupName* : an identifier for a set of surveys / HITs
* *time* : the time survey was taken.

Amazon Mechanical Turk terminology
----------------------------------

HITs (Human Intelligence Tasks) are initialized with a certain number of *assignments* (cf. "requests" in TurkGate lingo). A worker who accepts a HIT accepts a single *assignment* in that HIT. For our purposes, these assignments have the following attributes:

* *WorkerId* : same as above
* *SubmitTime* : the time the survey was submitted

Using TurkGateManager
---------------------

Download the turkgatemanager module and use in an interactive python session.

Requirements
^^^^^^^^^^^^

- `boto <https://github.com/boto/boto>`_
- `sqlalchemy <http://www.sqlalchemy.org/download.html>`_
