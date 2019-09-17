#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import numpy as np

try:
    import oct2py
    octave = oct2py.Oct2Py()
except:
    octave = None


################### Octave ####################


def pullFromOctave(aOct, varnames, localsDict, flatten=False):
    varnames = varnames.split(",")
    varnames = [(vn[1:] if vn[0]=='[' else (vn[:-1] if vn[-1]==']' else vn)).strip() for vn in varnames]
    for vn in varnames:
        tmp = aOct.pull(vn)
        try:
            tmp = tmp.flatten() if flatten else tmp
        except:
            pass
        localsDict[vn] = tmp



class Octave(object):
    @classmethod
    def unique(cls, mat):
        if Utils.isMatrix(mat):
            allElmts = mat.A1
        else:
            allElmts = []
            try:
                # if mat is composed like a matrix, with several iterables
                allElmts = [cell for row in mat for cell in row]
            except:
                # if mat is a vector
                allElmts = mat
        # elements = list(set(allElmts))
        elements = set(allElmts)
        return elements
    
    @classmethod
    def find(cls, mat):
        res = None
        raise Exception("Not implemented")
        return res
    
    @classmethod
    def compare(cls, mat1, mat2, comparator=(lambda a_ij,b_ij: a_ij == b_ij)):
        raise Exception("NO IMP")
        return None
        
    @classmethod
    def isvector(cls, elmt, considerListAsVector=False):
        return octave.isvector(elmt)
                


class Utils(object):
    @classmethod
    def isMatrix(cls, elmt):
        return isinstance(elmt, np.matrixlib.defmatrix.matrix)
    
    @classmethod
    def isMatrixLike(cls, elmt):
        return cls.isMatrix(elmt) or isinstance(elmt, np.ndarray)
    
    # @classmethod
    # def asMatrix(cls, elmt, *args):
    #     pass
        

