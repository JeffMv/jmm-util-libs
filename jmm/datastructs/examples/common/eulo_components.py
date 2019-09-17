"""
"""

from atom.api import Atom, Unicode, Range, Bool, Value, Int, Str, Tuple, List, observe


# class Strategy(object):
class Strategy(Atom):
    
    #
    # Bourse: utiliser les choses les plus faciles à faire
    # 
    @classmethod
    def isFrameContainingConfiguration(cls, frame, univers):
        """
        Déterminer si cette frame contient une configuration que la stratégie accepte.
        """
        pass
    
    # @classmethod
    # def frameIsContainingVisibleStuff(cls):
    #     """
    #     Déterminer 
    #     """
    #     pass
    
    pass


def etudier():
    """
    
    Je veux que cette méthode fasse quelque chose comme:
        - iterer sur les frames de tirages (pour une taille de frame donnée)
        - 
        - 
    """
    pass




class CTRule(Atom):
    """
    """
    name = Str()
    gameId = Str()
    minnb = Int()
    maxnb = Int()
    minet = Int()
    maxet = Int()
    
    universes = List()
    pickCounts = List()
    
    def __init__(self, universes, pickCounts, name="", gameId=None):
        """
        !param pickCounts: number of picked symbols without putting the symbol back.
        
        example Euromillions: CTRule( [{1,...,50}, {1,..12}], [5,2] )
        """
        super(CTRule, self).__init__()
        self.universes = universes
        self.pickCounts = pickCounts
        self.gameId = gameId
        self.minnb = min(universes[0])
        self.maxnb = max(universes[0])
        self.minet = min(universes[-1])
        self.maxet = max(universes[-1])
        self.name = name
    
    def universeForSymbolSet(self, index):
        return self.universes[index] if index < len(self.universes) else None
    
    def pickingCount(self, targetPoolIndex):
        return self.pickCounts[targetPoolIndex]
    
    def hasPickOnesOnly(self, targetPoolIndex):
        for pc in self.pickCounts:
            if pc > 1:
                return False
        return True
    
    def theoreticalGap(self, targetPoolIndex):
        res = len(self.universeForSymbolSet(targetPoolIndex)) / self.pickingCount(targetPoolIndex)
        res = round(res, 0)
        res = int(res)
        return res
    
    @classmethod
    def ruleForGameId(cls, gameId):
        if gameId=='triomagic':
            return CTRule.PredefinedRules.triomagicRule()
        elif gameId=='be-jokerplus':
            return CTRule.PredefinedRules.be_jokerplusRule()
        raise Exception("Unknown game id")
    
    
    class PredefinedRules(object):
        @classmethod
        def triomagicRule(cls):
            symbolsSet = set( list(range(0,10)) )
            univs = [symbolsSet.copy(), symbolsSet.copy(), symbolsSet.copy()]
            picks = [1 for el in univs]
            return CTRule( univs , picks )
        
        @classmethod
        def magic4Rule(cls):
            symbolsSet = set( list(range(0,10)) )
            univs = [symbolsSet.copy(), symbolsSet.copy(), symbolsSet.copy(), symbolsSet.copy()]
            picks = [1 for el in univs]
            return CTRule( univs , picks )
        
        @classmethod
        def be_jokerplusRule(cls):
            s = set( list(range(0,10)) )
            astro = set( list(range(1,12)) )
            univs = [s.copy(), s.copy(), s.copy(), s.copy(), s.copy(), s.copy(), astro]
            picks = [1 for el in univs]
            return CTRule( univs , picks )
    
