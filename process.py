# -*- coding: utf-8 -*-
"""PPKS ADAPTIVE TRAINING ENGINE: Data Processing

A collection of methods for cleaning up data retrieved from the databases.
Before data can be presented to a machine learning algorithm, it needs to 
properly cleaned, possibly normalized, and arranged into matrices and 
vectors.


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
from sklearn import preprocessing
import numpy as np 

def clean_data(X):
    ''' e.g. Deal with NaNs or blank entries, create dictionaries, deal
    with string values, etc. '''

    pass

def scale_features(X):
    ''' e.g. if data varies dramatically along different dimensions, we need
    to perform feature scaling. Use scikit-learn's feature scaling tool to
    return a scaled matrix of features with mean feature value of 0 and
    standard deviation of 1.'''
    
    X_scaled = preprocessing.scale(X)
    
    return X_scaled

