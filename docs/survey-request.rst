SurveyRequest
=============

SurveyRequest is the default MySQL database setup by TurkGate.

A participant taking a survey is associated with a single row in the MySQL database called a *request*. Each *request* has the following attributes:

* *workerID* : a unique identifier for each worker provided by Amazon
* *URL* : the URL of the survey
* *groupName* : an identifier for a set of surveys / HITs
* *time* : the time survey was taken.

+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+===========+==============+======+=====+=========+================+
| requestID | int(11)      | NO   | PRI | NULL    | auto_increment |
+-----------+--------------+------+-----+---------+----------------+
| workerID  | varchar(256) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
| URL       | varchar(256) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
| groupName | varchar(256) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
| time      | datetime     | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+

.. autoclass:: SurveyRequest
    :members:
