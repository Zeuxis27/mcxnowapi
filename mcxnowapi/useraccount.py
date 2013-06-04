# -*- coding: utf-8 -*-
#
# Module UserAccount for mcxnowapi - Python 27
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

class UserCurrencyAccount():
    #
    # UserCurrencyAccount : class with the info of the account of one currency of the user
    #
    def __init__(self, cur):
        self.Currency=cur
        self.Balance=0
        self.Incoming=0
        self.DepositAddress=None
        self.MinimumDeposit=0
        self.DepositConfirmations=0
        self.WithdrawFee=0

class UserDetails():
    #
    # UserDetails : class with all the info of the account of user
    #    
    def __init__(self,):
        self.Funds={}
        for cur in McxNowCurrency().GetCodeAll():
            self.Funds[cur]=UserCurrencyAccount(cur)

    def GetInfo(self, cur):
        if cur in McxNowCurrency().GetCodeAll():
            return  [self.Funds[cur].Currency,
            self.Funds[cur].Balance,
            self.Funds[cur].Incoming, 
            self.Funds[cur].DepositAddress, 
            self.Funds[cur].MinimumDeposit, 
            self.Funds[cur].DepositConfirmations, 
            self.Funds[cur].WithdrawFee
            ]
        else:
            return None

