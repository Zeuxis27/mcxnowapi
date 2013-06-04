# -*- coding: utf-8 -*-
#
# Module PublicOrder for mcxnowapi - Python 27
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

from mcxnowcurrency import McxNowCurrency


class PublicOrder():
    #
    # One Order 
    #
    def __init__(self, type, price,  amt, amtBTC):
        self.Type=type #str Sell or Buy
        self.Amount=amt #float
        self.AmountBTC=amtBTC #float
        self.Price=price #float


class PublicOrdersCurrency():
    #
    # List of all orders in a currency
    #
    def __init__(self):
        self.Id=[]
        
    def AddOrder(self, type, price, amt,  amtBTC):
        self.Id.append(PublicOrder(type, price, amt, amtBTC))
        
    def ClearList(self):
        del self.Id[:]


class PublicAllOrders():
    #
    # List of All orders of all the currency
    #
    def __init__(self):
        self.Orders={}
        self.ClearAllOrders()
        
    def AddOrder(self, cur, type, price, amt, amtBTC):
        if self.Orders[cur]==None:
            self.Orders[cur]=PublicOrdersCurrency()
        self.Orders[cur].AddOrder(type, price, amt, amtBTC)
        
    def ClearOrders(self, cur):
        self.Orders[cur]=None

    def ClearAllOrders(self):
        self.Orders={}
        for cur in McxNowCurrency().GetCodeAllTraded():
            self.Orders[cur]=None        
