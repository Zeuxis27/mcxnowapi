# -*- coding: utf-8 -*-
#
# Module McxNowConstants for mcxnowapi - Python 27
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

MCXNOW_DOMAIN="https://mcxnow.com"
MCXNOW_ALLCURRENCY=McxNowCurrency().GetCodeAll()
MCXNOW_TRADEDCURRENCY=McxNowCurrency().GetCodeAllTraded()

MCXNOW_ACTION={'login':'/index.html?login', 
                        'logout':'/action?logout', 
                        'useraccount':'/user.html', 
                        'trade':'/action?trade', 
                        'exchange':'/exchange/', 
                        'info':'/info?', 
                        'canceltrade':'/action?canceltrade', 
                        'exectrade':'/action?exectrade', 
                        'ordersbook':'/orders?', 
                        'chat':'/chat?', 
                        'sendchat':'/action?chat'
                        }

MCXNOW_ERROR={'Unknown':0,
                  'Ok':1, 
                  'No UserName':101, 
                  'No Password':102,
                  'Session ended':110,  
                  'Anonymous connexion':1000,
                  'Already Disconnected': 1100, 
                  'Unknown Currency':2000,
                  'HTTP Error':10000, 
                  'Trade Error No Enough Coins':20000, 
                  'Trade Error Minimum Request':20001, 
                  'Trade Error Price below minimum':20002, 
                  'Trade Error Order not send':20003, 
                  'Trade Error Ten Order already':20004, 
                  'Trade Error Type Error':20005, 
                  'Trade Error Currency not accepted':20006,
                  'Trade Error Confirm':20007, 
                  'Confirm Error Already Confirmed':30001, 
                  'Confirm Error No order with this id':30002
                  }
                  
