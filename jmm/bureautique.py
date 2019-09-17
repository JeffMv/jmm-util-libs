#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import os, sys

import csv, xlrd

################### Utils ####################


#https://www.powerball.net/numbers/1992-07-01
 
def csv_from_excel(excelFilepath, destCsvFilepaths, sheetPages):
    """
    """
    sheetPages = [sheetPages] if not isinstance(sheetPages, list) else sheetPages
    destCsvFilepaths = [destCsvFilepaths] if not isinstance(destCsvFilepaths, list) else destCsvFilepaths
    
    wb = xlrd.open_workbook(excelFilepath)
    for sheetName,csvFpath in zip(sheetPages, destCsvFilepaths):
        # csvFpath = destCsvFilepaths[i]
        
        sh = wb.sheet_by_name(sheetName)
        your_csv_file = open(csvFpath, 'wb')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        your_csv_file.close()



