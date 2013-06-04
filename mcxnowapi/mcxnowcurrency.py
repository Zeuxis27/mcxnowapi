# -*- coding: utf-8 -*-
#
# Module mcxnowcurrency for mcxnowapi - Python 27
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

from currency import Currency

class McxNowCurrency(Currency):
    def __init__(self):
        Currency.__init__(self)
        self.Add("BTC", "Bitcoin", 0)
        self.Add("MNC", "MinCoin", 1)
        self.Add("LTC", "Litecoin", 1)
        self.Add("SC", "SolidCoin", 1)
        self.Add("DVC", "Devcoin", 1)
        self.Add("WDC", "WorldCoin", 1)

class McxNowTradedCurrency():
    #
    # Info of traded currency
    #
    def __init__(self):
        self.Currency={}
        for cur in McxNowCurrency().GetCodeAll():
            self.Currency[cur]=TradedOneCurrency()
            
    def Add(self, cur, vol, volBTC, lastprice, pricel, priceh):
        self.Currency[cur].Volume=vol
        self.Currency[cur].VolumeBTC=volBTC
        self.Currency[cur].LastPrice=lastprice
        self.Currency[cur].PriceLow=pricel
        self.Currency[cur].PriceHigh=priceh

class TradedOneCurrency():
    #
    # Info of one traded currency
    #
    def __init__(self):
        self.Volume=0
        self.VolumeBTC=0
        self.LastPrice=0
        self.PriceLow=0
        self.PriceHigh=0
        
    def GetInfo(self):
        return([self.Volume, self.VolumeBTC, self.LastPrice, self.PriceLow, self.PriceHigh])
