#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for applying basic operations, computation, transformations to data in an immutable manner.
"""

import enum

from Operations import statistics as statsOps

import jmm
from jmm.divers import overrides

class Operation(object):
    """docstring for Operation"""
    
    # def __init__(self, operationFunc=None, name="operation", phrasingWords="operation on", operationMethod=None):
    def __init__(self, operationFunc, name="operation", phrasingWords="operation on"):
        super(Operation, self).__init__()
        
        self.operationFunc = operationFunc
        # self.operationMethod = operationMethod
        self.name = name
        self.phrasingWords = phrasingWords
        pass
    
    def applyToDataTable(self, data):
        """
        :return: an operation with processedData
        """
        # history = self._transformation(data)
        if data.history is None:
            history = TransformationsHistory( data, self, None )
        else:
            history = TransformationsHistory( data, self, data.history )
        
        # resultRows = self.operationFunc( data.getRows() ) # result of 
        resultRows = self._applyFunc( data )
        # if self.operationFunc:
        #     resultRows = self.operationFunc( data.getRows() ) # result of 
        # elif self.operationMethod:
        #     resultRows = self.operationMethod( data.getRows() ) # result of     
        
        tableName = self.nameForData( data.name )
        newTable = DataTable( rows=resultRows, history=history, name=tableName )
        
        return newTable
    
    # def _transformation(self, data):
    #     if data.history is None:
    #         history = TransformationsHistory( data, self, None )
    #     else:
    #         history = TransformationsHistory( data, self, data.history )
    #     return history
    
    def _applyFunc(self, data ):
        resultRows = self.operationFunc( data.getRows() ) # result of 
        return resultRows
        
    
    def nameForData(self, dataName):
        """Par exemple, 'effectif de $abc', où $abc est...
        """
        return "%s ( %s )" % (self.phrasingWords, dataName)
        
    class Complexity(enum.Enum):
        Instant  = 0b00001 # O(1) # 
        Fast     = 0b00010 # up to O( n * log(n) ) # 
        Slow     = 0b00100 # O( n * n ) # Quadratic
        VerySlow = 0b01100 # O( n ** k ), k >= 2 # polynomial
        Slug     = 0b10000 # O( k ** n ) : exponential
        pass


class ParametricOperation(Operation):
    """docstring for ParametricOperation"""
    def __init__(self, operationFunc, name="operation", phrasingWords="operation on", **kwargs):
        super(ParametricOperation, self).__init__(operationFunc, name, phrasingWords)
        self._forwardedParams = kwargs
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    @overrides(Operation)
    def _applyFunc(self, data):
        # print("in child method")
        resultRows = self.operationFunc( data.getRows() , **self._forwardedParams ) # result of 
        return resultRows
    
    # def _transformation(self, data):
    #     if data.history is None:
    #         history = TransformationsHistory( data, self, None )
    #     else:
    #         history = TransformationsHistory( data, self, data.history )
    #     return history



class TransformationsHistory(object):
    """docstring for TransformationsHistory
    
    - state: the state 
    - history: the previous history stack
    - operation: the operation that lead from history.state to this state
    """
    def __init__(self,  state, operation, history):
        super(TransformationsHistory, self).__init__()
        assert isinstance(history, TransformationsHistory) or  history is None
        
        self.history = history
        self.operation = operation
        self.state = state
    
    def previousData(self):
        """
        """
        prev = self.history
        if prev:
            tmp = self.history.state
            return tmp if tmp else None
        else:
            return None
    
    def length(self):
        """Number of states the user can rollback to"""
        i = 0
        cur = self.previousData()
        while cur is not None:
            i += 1
            cur = cur.previousData()
        return i
        
    
    def __str__(self):
        s = "state.name: %s, operation.name: %s, length: %i" % (self.state.name, self.operation.name, self.length())
        return s
    
    def __repr__(self):
        s = "TransformationsHistory < state.name: %s, operation.name: %s, length=%i >" % (self.state.name, self.operation.name, self.length())
        return s
        

class DataHyperTable(object):
    """docstring for DataHyperTable
    This class is meant to allow combining tables for concurrent use.
    For instance, instead of using 4 tables for studying OHLC trading data -one for each number stream-, one would want to combine them into single graphs for comparing trends/phenomena/differences/similarities between measures of Open and High prices.
    
    Basically, one implementation could be to have internaly N DataTable and apply chosen operations on each table separately, then when requested rows, have a function to merge table rows into one object (like DataFrame).
    """
    def __init__(self):
        super(DataHyperTable, self).__init__()
        raise UnboundLocalError("Unimplemented")
        

class DataTable(object):
    """docstring for DataTable
    
    Use cases:
    """
    def __init__(self, rows=None, history=None, name=None):
        super(DataTable, self).__init__()
        self.history = history
        self.name = "original" if name is None else name
        
        if (rows is None) and history:
            self.rows = history.state
        else:
            # Conformity assessment before assigment
            nonDataRows = [i for i,r in enumerate(rows) if not isinstance(r, DataTable.DataRow)]
            assert len(nonDataRows) == 0
            
            self.rows = rows if rows else []
        
    
    def transformed(self, operation):
        return operation.applyToDataTable(self)
    
    def contentAsList(self, sorted=False, reverse=False):
        """
        :param:
        """
        arr = [row.data for row in self.rows]
        arr = arr if not sorted else sorted(arr, key=lambda row: row.sortKey, reverse=reverse)
        return arr
    
    def contentIds(self, sorted=False, reverse=False):
        """
        :param:
        """
        arr = [row.id for row in self.rows]
        arr = arr if not sorted else sorted(arr, key=lambda row: row.sortKey, reverse=reverse)
        return arr
    
    def getRows(self):
        # return self.rows.copy()
        return self.rows
    
    def addContent(self, iterator):
        fromIndex = 1 + max([r.id for r in self.getRows()])
        for i, val in enumerate(iterator):
            index = fromIndex + 1
            row = DataTable.DataRow( index , val )
            self.rows.append(row)
        pass
    
    def previousStep(self):
        return (self.history.state) if self.history else None
    
    @classmethod
    def assertAreDataRows(cls, elmts):
        pass
    
    @classmethod
    def tableWith(cls, valuesIterator, idsIterator=None, sortKeyIterator=None):
        """
        """
        # No longer the case (#        :warning: The convention is to consider index 0 as the oldest element. This is in contradiction with some other modules but since this model is more general purpose, then it is the choice)
        values = list(valuesIterator)
        ids = list(idsIterator) if idsIterator else None
        sortKeys = list(sortKeyIterator) if sortKeyIterator else None
        rows = []
        for i,el in enumerate(values):
            # elId =  len(values) - i # our convention: at index 0 is the newest
            elId = ids[i] if ids else i
            elSortKey = sortKeys[i] if sortKeys else None
            r = DataTable.DataRow( elId, el, elSortKey )
            
            rows.append( r )
        return DataTable(rows)
    
    def columnsSpanCount(self):
        length = 1 if self.rows and len(self.rows)>0 else 0
        for row in self.rows:
            nl = row.columnsCount()
            if nl > length:
                length = nl
        return length
    
    def rowsCount(self):
        return len(self.rows)
    
    def rowAt(self, rowIndex):
        try:
            return self.rows[rowIndex]
        except:
            return None
    
    def elementAt(self, rowIndex, columnIndex):
        try:
            row = self.rows[rowIndex]
            return row.elementAt(columnIndex)
        except IndexError:
            return None
    
    def __str__(self):
        s = """DataTable(name: "%s", previous states: %i, rows: [%s,\n  ...] )""" % (self.name, (self.history.length() + 1) if self.history else 0, ",\n  ".join([str(r) for r in self.rows[:5]]) )
        return s
    
    def __repr__(self):
        s = "DataTable(rows=%s, history=%s, name='%s')" % (self.rows, self.history, self.name)
        return s
    
    class DataRow(object):
        def __init__(self, id, data, sortKey=None):
            super(DataTable.DataRow, self).__init__()
            self.id = id
            self.sortKey = id if sortKey is None else sortKey
            self.data = data
        
        def getData(self):
            return self.data
        
        def contentAsList(self):
            try:
                return list(self.data)
            except:
                return [self.data]
        
        def elementAt(self, columnIndex=0):
            try:
                return self.data[columnIndex]
            except:
                if columnIndex == 0:
                    return self.data
                else:
                    return None
        
        def columnsCount(self):
            d = self.data
            length = 1 if d else 0
            nl = 0
            try:
                nl = len(d)
            except:
                try:
                    nl = len(list(d))
                except:
                    pass
            if nl > length:
                length = nl
            return length
        
        def __str__(self):
            # s = "DataTable.DataRow < id: %s, sortKey: %s, data: %s >" % (self.id, self.sortKey, str(self.data))
            # return s
            return repr(self)
        
        def __repr__(self):
            """__repr__
            Called by the repr() built-in function and by string conversions (reverse quotes) to compute the "official" string representation of an object. If at all possible, this should look like a valid Python expression that could be used to recreate an object with the same value (given an appropriate environment).
            """
            s = "DataTable.DataRow(id=%s, data=%s%s)" % (self.id, str(self.data), "" if self.id==self.sortKey else (", sortKey=%s" % str(self.sortKey) ) )
            return s
    


# class ProcessingUnit(object):
#     """docstring for ProcessingUnit"""
#     def __init__(self):
#         super(ProcessingUnit, self).__init__()
    
#     def applyOperation(self, operation):
#         """
#         Changes the internal state of the data.
#         """
#         pass
    

def main():
    # data = DataTable()
    # data = data.transformed( Operations.statistics.effectif )
    # data = data.transformed( statsOps.effectif )
    pass

if __name__ == '__main__':
    main()




################################################################
####            A    I M P L E M E N T E R                   ###
################################################################


class BasicOperations(object):
    """docstring for BasicOperations"""
    def __init__(self):
        super(BasicOperations, self).__init__()
    
    @classmethod
    def reverseFunc(cls, data):
        res = list(reversed( data ))
        return res
    
    @classmethod
    def selectFunc(cls, table, firstN=None, lastN=None, indexes=None, withoutIndexes=None):
        inds = set()
        if firstN:
            inds = inds | set(list(range(firstN)))
        if lastN:
            inds = inds | set( list(range( len(table.rows), len(table.rows)-lastN, -1 )) )
        if indexes and len(indexes) > 0:
            inds = inds | set(indexes)
        if withoutIndexes:
            inds = inds - set(withoutIndexes)
        
        # must be an error
        if indexes is None and len(inds)==0:
            print("Warning :: selectFunc :: no selection was done.")
            inds = list(range(len(table.rows)))
        
        print("Should sort using the sort key (not the index)")
        sortedIndexes = sorted(inds, key=lambda r: r.sortKey if r.sortKey is not None else r.id)
        
        res = []
        for ind in sortedIndexes:
            res.append( table.rows[ind] )
        
        return res
    
    #############################
    
    @classmethod
    def reverseOperation(cls):
        name = "reverse"
        phrasingWords = "reverse of"
        op = Operation(cls.reverseFunc, name, phrasingWords)
        return op
    
    @classmethod
    def selectOperation(cls, firstN=None, lastN=None, indexes=None, withoutIndexes=None):
        """
        """        
        op = Operation(cls.selectFunc, "selection", "data selection of")
        return op



class StatisticsOperations(object):
    """docstring for StatisticsOperations"""
    def __init__(self):
        super(StatisticsOperations, self).__init__()
    
    @classmethod
    def sumRowFunc(cls, tableRows):
        res = []
        for row in tableRows:
            tmp = sum( row.contentAsList() )
            # drow = DataTable.DataRow( row.id, tmp )
            drow = DataTable.DataRow( row.id, tmp, row.sortKey )
            res.append( drow )
        return res
    
    @classmethod
    def effectifFunc(cls, tableRows, frame=None):
        universe = set( jmm.divers.flattenIterable([r.data for r in tableRows]) )
        if frame and (frame >= 1):
            filteredRows = [tableRows[i] for i in range( frame )]
        else:
            filteredRows = tableRows
        # print(len(filteredRows), frame)
        
        filteredData = [r.data for r in filteredRows]
        data = []
        for rowData in filteredData:
            try:
                data += list(rowData)
            except:
                data += [rowData]
        xis, nis = jmm.divers.effectifU(data, universe, returnSplitted=True)
        
        res = []
        for i, x in enumerate(xis):
            elId = x
            key = x
            val = nis[i]
            
            row = DataTable.DataRow( elId, val, key )
            res += [row]
        res.sort(key=lambda x: x.sortKey)
        return res
    
    
    @classmethod
    def currentGapFunc(cls, tableRows, frame=None):
        universe = set( jmm.divers.flattenIterable([r.data for r in tableRows]) )
        if frame and (frame >= 1):
            filteredRows = [tableRows[i] for i in range( frame )]
        else:
            filteredRows = tableRows
        # print(len(filteredRows), frame)
        
        filteredData = [r.contentAsList() for r in filteredRows]
                
        d = {}
        for i, symbol in enumerate(universe):
            for j,row in enumerate(filteredData):
                if symbol in row:
                    d[symbol] = j + 1
                    break
            if list(d).count(symbol)==0:
                if frame and frame >= 1:
                    d[symbol] = (frame + 1)
                else:
                    d[symbol] = len(filteredData) + 1
        
        res = []
        for key in d:
            elId = key
            val = d[key]
            row = DataTable.DataRow( elId, val, key )
            res += [row]
        res.sort(key=lambda x: x.sortKey)
        return res
    
    @classmethod
    def currentParityFunc(cls, tableRows, frame=None):
        if frame and (frame >= 1):
            filteredRows = [tableRows[i] for i in range( frame )]
        else:
            filteredRows = tableRows
        # print(len(filteredRows), frame)
        
        filteredData = [r.contentAsList() for r in filteredRows]
        
        filteredData = [r.data for r in filteredRows]
        
        data = []
        for rowData in filteredData:
            try:
                data += list(rowData)
            except:
                data += [rowData]
        
        data = jmm.divers.flattenIterable(data)
        
        nbrEven = len([i for i in data if (i % 2)==0])
        nbrOdd  = len([i for i in data if (i % 2)==1])
        
        rowOdd  = DataTable.DataRow( 1, nbrOdd, 1 )
        rowEven = DataTable.DataRow( 2, nbrEven, 2 )
        
        res = [rowOdd, rowEven]
        return res
    
    
    #############################

    @classmethod
    def sumRowOperation(cls):
        op = Operation(cls.sumRowFunc, "row sum", "row sum on")
        return op
    
    @classmethod
    def effectifOperation(cls, frame=None):
        op = ParametricOperation(cls.effectifFunc, name="effectif", phrasingWords="effectif de", frame=frame)
        # print( "op.frame:", op.frame )
        return op
    
    @classmethod
    def currentGapOperation(cls, frame=None):
        op = ParametricOperation(cls.currentGapFunc, name="ecart", phrasingWords="ecart de", frame=frame)
        # print( "op.frame:", op.frame )
        return op
    
    @classmethod
    def currentParityOperation(cls, frame=None):
        op = ParametricOperation(cls.currentParityFunc, name="parité", phrasingWords="parité de", frame=frame)
        return op
    


class SelectionOperation(ParametricOperation):
    """docstring for SelectionOperation"""
    def __init__(self, firstN=0, lastN=0, indexes=[], withoutIndexes=[]):
        super(SelectionOperation, self).__init__( BasicOperations.selectFunc, "selection", "data selection of")
        self.firstN = firstN
        self.lastN = lastN
        self.indexes = indexes
        self.withoutIndexes = withoutIndexes
        self.operationFunc = BasicOperations.selectFunc


class ComputationOperation(Operation):
    """docstring for ComputationOperation
    
    ... split hi¨: bool
    """
    def __init__(self):
        super(ComputationOperation, self).__init__()
        pass

class PreprocessingOperation(Operation):
    """docstring for PreprocessingOperation"""
    def __init__(self):
        super(PreprocessingOperation, self).__init__()
        

class OperationChain(object):
    """docstring for OperationChain"""
    def __init__(self, arg):
        super(OperationChain, self).__init__()
        self.arg = arg
        

