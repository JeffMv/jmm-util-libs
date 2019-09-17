#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

from .divers import *

from bs4 import BeautifulSoup

import statistics


################### Soupification ####################

def soupify(elmt, *args, **kwargs):
    """
    :param elmt:
    :param encoding: ... default 'utf-8'
    """
    soup = None
    if isinstance(elmt, bytes):
        encoding = kwargs.get('encoding')
        encoding = encoding if encoding else 'utf-8'
        elmt = elmt.decode(encoding=encoding)
    else:
        ### Consider it might be a `requests` Response object
        try:
            requestsResponse = elmt
            elmt = requestsResponse.content.decode(encoding=requestsResponse.encoding)
        except:
            pass
    soup = soupifyContent(elmt)
    return soup

def soupifyContent(content, clearWhitespaces=False):
    """Creates a BeautifulSoup soup with the provided content
    :param content: the content to parse as a string
    :param clearWhitespaces: removes unnecessary whitespaces in the html
            (otherwise parsed and outputed when calling soup.get_text() for
            instance).
    :return: a BeautifulSoup object parsed.
    """
    if clearWhitespaces:
        content = content.replace("  ","").replace("\n\n","").replace("\t","")
    return BeautifulSoup(content, 'lxml')

def soupifyRequestsResponse(resp, *args, **kwargs):
    content = resp.content.decode(encoding=resp.encoding)
    return soupify(content, *args, **kwargs)

def soupifyFile(filepath, *args, **kwargs):
    with open(filepath, "r") as f:
        content = f.read()
        soup = soupify(content, *args, **kwargs)
    return soup



#######   AUTOMATIC   ARTICLE   NODE   DETECTION   #######

def getIdAndClasses(tag):
    try:
        tId = tag['id']
    except KeyError:
        tId = None
    #
    try:
        tClasses = tag['class']
    except:
        tClasses = []
    #
    return {'id': tId, 'class':tClasses}


def getClassHistogram(aSoup):
    allTags = aSoup.find_all(True)
    #basicAttrs = [getIdAndClasses(tag) for tag in allTags]
    classes = [tag['class'] for tag in allTags if tag.get('class')]
    allClasses = []
    for cs in classes:
        allClasses += cs
    # faire statistique
    _hist = effectif(allClasses)
    uclasses = [key for key in list(_hist)]
    nbrs = [_hist[key] for key in list(_hist)]
    #
    oNbrs = sorted(nbrs, reverse=True) # greatest first
    _perm = getPermutation(nbrs, oNbrs)
    oclasses = applyPermutation(uclasses, _perm)
    return (oclasses, oNbrs)


def filterClassesHistogram(aSoup, minNbrOccurrences=None, maxNbrOccurrences=None):
    """
    :param aSoup:
    :param minNbrOccurrences:
    :param minNbrOccurrences:
    :return: classes, counts
    """
    cls,nbr = getClassHistogram(aSoup)
    _min = minNbrOccurrences if minNbrOccurrences!=None else min(nbr)
    _max = maxNbrOccurrences if maxNbrOccurrences!=None else max(nbr)
    indices = [i for i, c in enumerate(cls) if (_min <= nbr[i] and nbr[i] <= _max)]
    classes = [cls[i] for i in indices]
    counts = [nbr[i] for i in indices]
    return classes, counts


def filterPossibleArticleRelatedClasses(aSoup, minNbrOccurrences=4, maxNbrOccurrences=None):
    """
    :param aSoup:
    :param minNbrOccurrences:
    :param maxNbrOccurrences:
    :return: classes, nbrs
    """
    # default value
    classes,nbrs = filterClassesHistogram(aSoup, minNbrOccurrences, maxNbrOccurrences)
    return classes,nbrs


def getMostPlausibleArticleClasses(aSoup, **kwargs):
    """For HTML soups containing articles/products. Analyses the soup and
    inferes what the classes of the product nodes must be.
    
    :param aSoup: HTML code containing at least the enclosing node of the
                articles/products you would like to retrieve.
    :param **kwargs: you may pass parameters for the helper method
                `filterPossibleArticleRelatedClasses` (min/max nbr of
                arguments, see the function docstring).
    
    :return: articleRelatedClasses, articleRelatedClassesOccurrences
                articleRelatedClasses: the most plausible classes that seem to
                    describe an article node.
                articleRelatedClassesOccurrences: the corresponding number of
                    occurances of the corresponding class
    """
    if 'minNbrOccurrences' in kwargs:
        regularMin = kwargs.get('minNbrOccurrences')
        # without this line, can cause TypeError for duplicate keyword argument error 
        kwargs.pop('minNbrOccurrences')
    else:
        regularMin = 6
    #
    classes,nbrs = filterPossibleArticleRelatedClasses(aSoup, minNbrOccurrences=regularMin, **kwargs)
    try:
        mostReccurentSetOfClassEff = statistics.mode(nbrs) # articles have the same classes for different tags in the hierarchy
    except statistics.StatisticsError:
        _dNsEffs = effectif(nbrs)
        _ns = list(_dNsEffs)
        _effs = [_dNsEffs[key] for key in _ns]
        mostReccurentSetOfClassEff = _ns[_effs.index( max(_effs) )]
    articleRelatedClasses = [classes[i] for i,n in enumerate(nbrs) if n==mostReccurentSetOfClassEff]
    articleRelatedClassesOccurrences = [nbrs[i] for i,n in enumerate(nbrs) if n==mostReccurentSetOfClassEff]
    return articleRelatedClasses, articleRelatedClassesOccurrences


def extractPlausibleArticleNodes(aSoup, tagNameRestrictionCollection=None, **kwargs):
    """Analyses a BeautifulSoup soup of an HTML page in order to infere and
    extract nodes that look like article nodes.
    The page provided must have several articles on it (for instance a catalog
    page).
    In general, this function can be used to find nodes of repeated similar
    things in an HTML page.
    
    :note: This function only works on elements that do not have
            It looks and analyses several things (the classes, ...)
    
    :param aSoup: some HTML code containing at least the enclosing markup
                of the elements that you would like to extract.
    :param tagNameRestrictionCollection: Classes that must the expected article
                nodes should contain.
                Especially useful to pick the expected set of article nodes
                if there are several different article catalogs/sections on the
                page.
                For instance, if you have performed a preliminary analysis and
                found out what classes the article nodes you look for have, you
                may specify it here.
    :param **kwargs: You may pass key-value arguments for the
                getMostPlausibleArticleClasses helper function.
    """

    def getMostEnclosingTag(tagNode, keyClasses):
        """Returns the outtermost tag that can be an article.
        """
        mostEnclosingTag = tagNode
        currentTag = tagNode
        while currentTag.parent!=None:
            currentTag = currentTag.parent
            # parent tags can be different from what we have in the 'tags' variable.
            # if the tag has the classes we were looking for in article tags, then it is a tag we want
            if currentTag.get('class') and len(set(currentTag.get('class')) & set(artClasses))>0:
                # this tag has what 
                mostEnclosingTag = currentTag
        return mostEnclosingTag
    
    ## We analyze and infere the CSS classes that are most likely used to
    ## describe articles in the soup.
    artClasses, artClassesOccurrences = getMostPlausibleArticleClasses(aSoup, **kwargs)
    
    ## Some old pages do not use class to describe articles. In those cases we
    ## cannot do anything with this approach.
    assert len(artClasses) > 0
    
    ## Boolean helpers
    # If provided with 1+ class restrictions, it only gets 
    match_tag_restriction = lambda tag: (tag.name in set(tagNameRestrictionCollection)) if (tagNameRestrictionCollection is not None) else True
    # 
    has_article_classes = lambda tag: (tag.get('class') is not None) and len(set(tag.get('class')) & set(artClasses)) > 0
    
    checker = lambda tag: match_tag_restriction(tag) and (tag.get('class') is not None) and 1 <= len(set(tag.get('class')) & set(artClasses))
    
    if tagNameRestrictionCollection:
        _tagNameRestr = set(tagNameRestrictionCollection)
        # 
        checker = lambda tag: (tag.name in _tagNameRestr) and tag.get('class') is not None and 1 <= len( set(tag.get('class')) & set(artClasses) )
        tags = aSoup.findAll(checker)
    else:
        scs = set(artClasses)
        tags = aSoup.findAll( lambda tag: tag.get('class') is not None and 1 <= len( set(tag.get('class')) & scs ) )
    
    plausibleArticleTags = set()
    for aTag in tags:
        mostEnclosingTag = getMostEnclosingTag(aTag, artClasses)
        plausibleArticleTags.add( mostEnclosingTag )
    #
    # tous les tags pour lesquels on a que
    # ( len( set() & set() ) / len( set() / set() ) ) >= 0.5
    # entre ce tag t et le tag de reference (mostEnclosingTag)
    #
    return list( plausibleArticleTags )


#######   / AUTOMATIC   ARTICLE   NODE   DETECTION   #######



