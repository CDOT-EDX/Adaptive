# -*- coding: utf-8 -*-
"""PPKS ADAPTIVE TRAINING ENGINE: Machine Learning Routines

A collection of methods for training a learning model on the data and
evaluating the performance of the model.


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
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix
try:
    import cPickle as pickle
except:
    print 'Failed to import cPickle. Falling back to pickle.'
    import pickle


# Define a helper function for calculating the root-mean-square error
def RMSE(y_true,y_pred):
    ''' The Root-Mean-Square Error takes the predicted values y_pred for the target
    variable y_true and takes the square root of the mean of the square of their
    differences. '''
    return np.sqrt(np.sum(np.square(y_pred-y_true))/len(y_true))

def performance_metrics(model,X,y,verbose=False):
    accuracy = cross_val_score(model,X,y,scoring='accuracy')
    precision = cross_val_score(model,X,y,scoring='precision')
    recall = cross_val_score(model,X,y,scoring='recall')
    f1 = cross_val_score(model,X,y,scoring='f1')

    score = [accuracy[0], precision[0], recall[0], f1[0]]
  
    if verbose:
        print 'Accuracy: the fraction of correct predictions'
        print accuracy[0]
        print 'Precision: aka Positive Prediction Rate, tp / (tp + fp)'
        print precision[0]
        print 'Recall: aka True Positive Rate, tp / (tp + fn)'
        print recall[0]
        print 'F-score: weighted avergae of precision and recall, F1 = 2 * (precision * recall) / (precision + recall)'
        print f1[0]
        return score 
    else:
        return score

def draw_confusion_matrix(y_true, y_pred, filename=None):
    ''' Draws the confusion matrix of the model outcomes and dumps
    it to a file with filename confusion_matrix.png unless otherwise
    specified.'''
    cm = confusion_matrix(y_true, y_pred)
    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    if filename:
        plt.savefig(filename)
    else:
        plt.savefig('confusion_matrix.png')

def train_model(X,y,n_ests):
    '''Trains a Random Forest regressor, which is an ensemble of decision tree regressors.
    Returns the model and the feature importances.'''
    model = RandomForestRegressor(n_estimators=n_ests, criterion='mse', max_depth=None, n_jobs=-1)

    print 'Training Random Forest regressor.'
    model.fit(X,y)

    return model, model.feature_importances_
