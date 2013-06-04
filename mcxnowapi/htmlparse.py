# -*- coding: utf-8 -*-
#
# Module HTMLParse for mcxnowapi - Python 27
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

from HTMLParser import HTMLParser

class UserAccountHTMLParser(HTMLParser):
    #
    # Parser for Account WebPage
    #
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundlevel = 0
        self.forbiddenlist=[' ','Withdraw To:','Withdraw Amount:', 'Confirm Withdraw', 'Deposit:']
        self.data=[]
        self.deposit=[]
        self.depositflag=False
        self.incoming={}
        for cur in McxNowCurrency().GetCodeAll():
            self.incoming[cur]=0
    def handle_starttag(self, tag, attrs):
        if self.foundlevel==0:
            if tag=='div':
                    for attr in attrs:
                        if attr[1]=='fundbox':
                            self.foundlevel=1
        else:
            if tag<>'input':
                self.foundlevel+=1
        
    def handle_endtag(self, tag):
        if self.foundlevel>0:
            self.foundlevel-=1

    def handle_data(self, data):
        if self.foundlevel>0:
            if (data not in self.forbiddenlist) and ('Incoming:' not in data):
                self.data.append(data)
            if 'Incoming:' in data:
                for cur in McxNowCurrency().GetCodeAll():
                    if cur in data:
                        self.incoming[cur]=float(data.split('Incoming:')[1].split(cur)[0])
        if self.depositflag:
            self.depositflag=False
            self.deposit.append(data)
        if ('minimum deposit:' in data) or ('withdraw fee:' in data) or ('confirmations needed:' in data):
            self.depositflag=True
            self.deposit.append(data)

