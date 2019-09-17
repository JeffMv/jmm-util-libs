#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of application using the Stateless Operations module.

"""

import json
import enum
import os
import datetime


# Import and setup enamlx before importing enaml
import enamlx # allow table views
enamlx.install()

import enaml
from enaml.qt.qt_application import QtApplication
from atom.api import Atom, observe, Unicode, Range, Bool, Value, Int, Str, Tuple, ContainerList


os.sys.path.append(os.path.dirname(os.getcwd()))
import StatelessOps as sops
from common import eulo_components as euloCpt


# class ComputationInfos:
#     pass

class PreferencesStorage(Atom):
    """
    """
    ############
    ### Adding settings:
    ###     just add the setting in the next 3 spots.
    ############
    
    ### Spot 1: Registering the setting by adding it as an attributes
    preferencesFilePath = Str("./prefs.json")
    dataPersistenceDir = Str("./persistence/windows")
    drawsfile = Str()
    gameId = Str()
    selectedRuleIndex = Int()
    # Preferences pour le prochain calcul
    selectedCPSymbolsSetChoiceIndex = Int()
    selectedCPVisualizationTypeIndex = Int()
    selectedCPOutputDataTypeIndex = Int()
    selectedCPMeasureIndex = Int()
    
    ### Spot 2: In order to load last setting
    def getCurrentPrefsAsDict(self):
        return {
            'preferencesFilePath':self.preferencesFilePath,
            'dataPersistenceDir': self.dataPersistenceDir,
            'drawsfile':self.drawsfile, "gameId": self.gameId, 'selectedRuleIndex':self.selectedRuleIndex,
            'selectedCPSymbolsSetChoiceIndex':self.selectedCPSymbolsSetChoiceIndex,
            'selectedCPVisualizationTypeIndex':self.selectedCPVisualizationTypeIndex, 'selectedCPOutputDataTypeIndex':self.selectedCPOutputDataTypeIndex, 'selectedCPMeasureIndex':self.selectedCPMeasureIndex
            }
    
    ### Spot 3: Notification on setting change (=> autosave when change)
    @observe(['drawsfile', 'gameId', 'dataPersistenceDir','selectedRuleIndex',
        'selectedCPSymbolsSetChoiceIndex',
        'selectedCPVisualizationTypeIndex','selectedCPOutputDataTypeIndex','selectedCPMeasureIndex'
        ])
    def processOnPropertyValueChange(self, change):
        """Save preferences when edit is made
        """
        self.savePrefsToFile( self.getCurrentPrefsAsDict(), self.preferencesFilePath )
    
    
    ############
    
    _sharedInstance = None
    
    @classmethod
    def sharedInstance(cls):
        if PreferencesStorage._sharedInstance is None:
            PreferencesStorage._sharedInstance = PreferencesStorage()
        return PreferencesStorage._sharedInstance
    
    sharedInstance.instance = None
    
    def __init__(self):
        super(PreferencesStorage, self).__init__()
        if os.path.isfile(self.preferencesFilePath):
            with open(self.preferencesFilePath, "r") as fh:
                prefs = json.load(fh)
        else:
            prefs = self.getCurrentPrefsAsDict()
            self.savePrefsToFile(prefs, self.preferencesFilePath)
        self.updatePrefsFromDict(prefs)
    
    def updatePrefsFromDict(self, prefs):
        for key in prefs:
            setattr(self, key, prefs[key])
    
    def savePrefsToFile(self, prefs, filepath, indent=2):
        try:
            with open(filepath, "w") as fh:
                json.dump(prefs, fh, indent=indent)
        except Exception as err:
            print("error while saving:",err)
            pass
    
    
class Delegate(object):
    pass


def fooLoadSloex(content):
    lines = content.strip().split("\n")
    fields = [line.split("\t") for line in lines if len(line.strip())>0]
    fromCol = 4
    
    draws = [ [int(symField) for symField in lineFields[fromCol:-2]] for lineFields in fields]
    ids = [int(lineFields[2]) for lineFields in fields]
    sortKeys = ids
    return draws, ids, sortKeys, None

def fooLoadEum(content, indexOfColumn=1, idColumnIndex=0,  fieldSep='\t', symbolSep=','):
    lines = content.strip().split('\n')
    head = lines[0]
    hasHeader = (head.lower().find("date") >= 0) or (head.lower().find('numeros') >= 0)
    hasDateColumn = head.lower().split(fieldSep).count('date')>0 if hasHeader else False
    dateColumnIndex = (head.lower().split(fieldSep).index("date")) if hasDateColumn else None
    lines = lines[1:] if hasHeader else lines
    
    symbolBlocks = [l.split(fieldSep)[indexOfColumn] for l in lines]
    ids = [l.split(fieldSep)[idColumnIndex] for l in lines]
    sortKeys = ids
    sdates = [l.split(fieldSep)[dateColumnIndex] for l in lines] if dateColumnIndex else None
    dates = [datetime.datetime.strptime(tmpsdate, '%d.%m.%Y') for tmpsdate in sdates] if sdates else None
    
    strToSymbolType = lambda s: int(s)
    # strToSymbolType = lambda s: s # pour super-star par ex
    draws = [ [strToSymbolType(sym) for sym in b.strip().split(symbolSep)] for b in symbolBlocks]
    return draws, ids, sortKeys, dates


class MyData(object):
    """docstring for MyData"""
    def __init__(self):
        super(MyData, self).__init__()
        self.lastOpenedPath = None
        self.draws = None
        self.ids = None
        self.dates = None
        self.sortKeys = None
        self.dataTable = None
    
    def openDrawsAtPath(self, path, indexOfColumn=1, idColumnIndex=0,  fieldSep='\t', symbolSep=',', gameId=None):
        draws = None
        ids, sortKeys, dates = None,None,None
        try:
            with open(path, 'r') as fh:
                content = fh.read()
            
            if gameId in ['eum', 'slo']:
                # draws, ids, sortKeys, dates = fooLoadEum(content, indexOfColumn=1, idColumnIndex=0,  fieldSep='\t', symbolSep=',')
                draws, ids, sortKeys, dates = fooLoadEum(content, indexOfColumn=indexOfColumn, idColumnIndex=idColumnIndex,  fieldSep=fieldSep, symbolSep=symbolSep)
            elif gameId in ['sloex']:
                draws, ids, sortKeys, dates = fooLoadSloex(content)
            else:
                print("unknown/unrecognized gameId '%s' at path %s" % (gameId, path))
        except FileNotFoundError:
            print("File not found at %s" % path)
        except Exception as err:
            print("MyData::openDrawsAtPath::error : ", err)
            raise err
            pass
        
        if draws is None and gameId is None:
            
            _gameIds = iter(['eum', 'slo', 'sloex'])
            
            tmpGameId = next(_gameIds)
            # while self.openDrawsAtPath(path,indexOfColumn, idColumnIndex, fieldSep, symbolSep, tmpGameId).draws is None and tmpGameId is not None:
            #     try:
            #         tmpGameId = next(_gameIds)
            #     except:
            #         tmpGameId = None
                
                
        
        self.lastOpenedPath = path
        self.draws = draws
        self.ids = ids
        self.dates = dates
        self.sortKeys = dates
        return self
    
    def toTable(self):
        try:
            self.dataTable = sops.DataTable.tableWith(self.draws, idsIterator=self.ids, sortKeyIterator=self.sortKeys)
        except:
            self.dataTable = None
        return self
    


class GameProbabilities(Atom):
    #
    trueNegatives = Int()
    # truePositives = Int()
    # bucketA = Int()
    # bucketB = Int()
    
    

##########################################


def main():
    app = QtApplication()
    
    # Import our Enaml EmployeeView
    with enaml.imports():    
        from eulo_graph_view import Preferences, ComputationLauncherMainBoard, DataTableTBV
    
    # Preferences and settings and model
    prefs = PreferencesStorage.sharedInstance()

    # gameId = "eum"
    gameId = "sloex"
    
    rule = euloCpt.CTRule(  [list(range(1,51)), list(range(1,13))] , [5,2] , name="Euromillions (formule 12 étoiles)", gameId=gameId )
    dataLoader = MyData().openDrawsAtPath(gameId, prefs.drawsfile).toTable()
    
    # Delegation of responses
    delegate = Delegate()
    delegate.getPreferencesModel = lambda : prefs
    delegate.getCustomRule = lambda : rule
    delegate.loadDrawsData = lambda launcherView, prefsModel, gameId: setattr( launcherView, 'dataModel', dataLoader.openDrawsAtPath(prefsModel.drawsfile, gameId=gameId).toTable().dataTable)
    
    ## Preferences window
    # view = Preferences(prefsModel=prefs, customRule=rule)
    
    view = ComputationLauncherMainBoard(prefsModel=prefs, delegate=delegate, dataModel=dataLoader.dataTable)
    view.show()
    if dataLoader.dataTable:
        DataTableTBV(model=dataLoader.dataTable, prefsModel=prefs).show()
    
    app.start()








##########################################

class Person(Atom):
    first_name = Str()
    last_name = Str()
    age = Int()
    debug = Bool()

class FooModel(Atom):
    people = ContainerList(Person)
    
    def add_person(self):
        #people = self.people[:]
        for i in range(100):
            age = len(self.people)
            person = Person(last_name='Doe-{}'.format(age),first_name='John-{}'.format(age),age=age)
            #people.append(person)
            self.people.insert(0,person)
    
    def remove_person(self):
        #people = self.people[:]
        #people.pop()
        self.people.pop()

data_model = FooModel(people=[
    Person(last_name='Barker-%i'%i,
           first_name='Bob%i'%i,
           age=i,
           debug=bool(i&1))
    for i in range(10) # 10000
])


if __name__ == '__main__':
    main()
