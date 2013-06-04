# -*- coding: utf-8 -*-
#
# Module UserOrder for mcxnowapi - Python 27
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

class UserOrder():
    #
    # One Order of the user
    #    
    def __init__(self, id, type, time, confirm, amt, price):
        self.Id=id #str
        self.Type=type #str Sell or Buy
        self.Time=time # time format Unix
        self.Confirmed=confirm # 1=confirmed 0= to confirm
        self.Amount=amt #float
        self.Price=price #float



class UserOrdersCurrency():
    #
    # All orders in a currency of the user
    #    
    def __init__(self):
        self.Id={}

    def AddOrder(self, id, type, time, confirm, amt, price):
        self.Id[id]=UserOrder(id, type, time, confirm, amt, price)
        
    def ClearList(self):
        self.Id={}
        
    def GetId(self):
        result=[]
        for i in self.Id:
            result.append(self.Id[i].Id)
        return result
    
    def GetOrderInfo(self, id):
        result=[]
        if id in self.GetId():
            result.append(self.Id[id].Id)
            result.append(self.Id[id].Type)
            result.append(self.Id[id].Time)
            result.append(self.Id[id].Amount)
            result.append(self.Id[id].Price)
        return result
        


class UserAllOrders():
    #
    # All orders of the user
    #
    def __init__(self):
        self.Orders={}
        self.BaseBalance={}
        self.CurrencyBalance={}
        self.ClearAllOrders()

        
    def AddOrder(self, cur, id, type, time, confirm, amt, price):
        if self.Orders[cur]==None:
            self.Orders[cur]=UserOrdersCurrency()
        self.Orders[cur].AddOrder(id, type, time, confirm, amt, price)
        
    def ClearCurrencyAllOrders(self, cur):
        self.Orders[cur]=None
        self.BaseBalance[cur]=0
        self.CurrencyBalance[cur]=0

    def ClearAllOrders(self):
        for cur in McxNowCurrency().GetCodeAllTraded():
            self.Orders[cur]=None
            self.BaseBalance[cur]=0
            self.CurrencyBalance[cur]=0
            
    def AddBaseBalance(self, cur, base_bal):
        self.BaseBalance[cur]=base_bal

    def AddCurrencyBalance(self, cur, cur_bal):
        self.CurrencyBalance[cur]=cur_bal            
