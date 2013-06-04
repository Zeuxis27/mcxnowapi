# -*- coding: utf-8 -*-
#
# Module currency for mcxnowapi - Python 27
# 
# Part of API for the crytpo market exchange mcxNow : https://mcxnow.com
#
# Copyright (c) 2013 Zeuxis : zeuxis27@gmail.com
# 
# Donations :
# BTC : 18ZqmXd8xzUtzAhDXZwBJQgyHV8Rxo7GV1
# LTC : LVjfq1JNvCX2qHLxTzQoEfRnh4EbdZui51
# MNC : MA6RGr42cioJsCkAYLt8kV5sxjiNfDh6si
# SC : sJwUHidU7x5o7kDDxPjXVKbYq3EpLca1iV
# WDC : Wk4j5PGzUWvm311H6TPcQwK3pzNMZknPjS
# FTC : 6zVjFJNJwBN3u6esi6uW54z3vY8L3hemCv
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License  
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
#


class Currency():
    def __init__(self):
        self.List=[]

    def GetAllTraded(self):
        #
        # Return a tuple of all currency traded
        #
        result=[]
        for cur in self.List:
            if cur.Traded==1:
                result.append(cur)
        return tuple(result)

    def GetAll(self):
        #
        # Return a tuple of all currency
        #
        result=[]
        for cur in self.List:
            result.append(cur)
        return tuple(result)

    def GetCodeAllTraded(self):
        #
        # Return a tuple of all code of currency traded
        #
        result=[]
        for cur in self.List:
            if cur.Traded==1:
                result.append(cur.Code)
        return tuple(result)


    def GetNameAllTraded(self):
        #
        # Return a tuple of all name of currency traded
        #
        result=[]
        for cur in self.List:
            if cur.Traded==1:
                result.append(cur.Name)
        return tuple(result)

    def GetCodeAll(self):
        #
        # Return a tuple of all code of currency
        #
        result=[]
        for cur in self.List:
            result.append(cur.Code)
        return tuple(result)

    def GetNameAll(self):
        #
        # Return a tuple of all name of currency
        #
        result=[]
        for cur in self.List:
            result.append(cur.Name)
        return tuple(result)

    def Add(self, code=None, name=None, traded=0):
        # Add a new currency
        if code<>None and name<>None:
            self.List.append(OneCurrency(code, name, traded))


class OneCurrency():
    def __init__(self, code=None, name=None, traded=0):
        self.Code=code
        self.Name=name
        self.Traded=traded


