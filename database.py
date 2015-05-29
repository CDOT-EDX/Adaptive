# -*- coding: utf-8 -*-
"""PPKS ADAPTIVE TRAINING ENGINE: Database Access Routines

A collection of methods for accessing the MySQL databases maintained by the edX
learning learning platform. It is necessary to retrieve information on student
performance both individual and collective. Information on students that have
completed a course and received a final grade is used to train a learning model
against which new students have their performance compared.


Example
-------
Include examples here of how the functions of this module are to be used:

    $ python example_numpy.py


Notes
-----
Include any notes here.


Attributes
----------
List all variables and functions here.

module_level_variable : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.

"""

import MySQLdb

def connect_to_db(db_name):
    ''' Form a database connection and return a database object. '''
    db_connection = MySQLdb.connect(host="localhost",   # your host, usually localhost
                                    user="john",        # your username
                                    passwd="pass",      # your password
                                    db=db_name)         # name of the data base
   
    return db_connection


def query_student_record(student_id,db):
    ''' Retrieve all the records of a single student '''
    # Create cursor object in order to execute SQL queries
    cur = db.cursor() 

    # Query student
    cur.execute("""SELECT %s FROM table""", (student_id,))
    
    rows = []
    for row in cur.fetchall():
        rows.append(row)

    return rows


def query_all_students(course):
    ''' Return the historical records of students who have completed a course. '''
    pass
