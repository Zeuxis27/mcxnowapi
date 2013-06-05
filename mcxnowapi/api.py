# -*- coding: utf-8 -*-
#
# Main Module for mcxnowapi - Python 27
# 
# API for the crytpo market exchange mcxNow : https://mcxnow.com
#
# Copyright (c) 2013 Zeuxis : zeuxis27@gmail.com
# 
# If you see some error, thanks to send me a mail
#
# Any suggestion are welcome
#
# For support my work, you can send me some coins ;-)
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

import requests
from request import request
import time

from mcxnowuser import McxNowUser
from mcxnowconstants import  *
from mcxnowpublic import McxNowPublic

from htmlparse import UserAccountHTMLParser
from mcxnowcurrency import McxNowCurrency

class McxNowSession():
    #---------------------------------------------------------------------------
    #
    # Class mcxnowsession :
    # 
    # Used to have access to mcxnow
    # 
    # Use :
    #
    # 1) mcxnowsession() : give you access to all data from mcxnow but you can trade : Anonymous connexion
    #
    # 2) mcxnowsession(username,password) : give you access to all data AND your account : you can trade !!!
    #
    #---------------------------------------------------------------------------
    
    def __init__(self,username=None, password=None ):
        self.Session=requests.Session()
        self.User=McxNowUser()
        self.Public=McxNowPublic()
        self.ErrorCode=0
        self.Return=None
        if self.Login(username, password):
            self.Trading=True
        else:
            self.Trading=False

    
    def __parseFloat__(self, texte):
        #
        # Convert a str to float : if success return float else return 0
        #
        try:
            nombre=float(texte)
        except:
            return 0
        else:
            return nombre
    
    def __getTime__(self, t=0, format="%a, %d %b %Y %H:%M:%S"):
        #
        # Return time t in the format (str)
        #
        return time.strftime(format,time.localtime(t))

    def __Login__(self):
        self.Return=None
        logindata={'user': self.User.UserName, 'pass': self.User.Password}
        result=request(self.Session, 'post', MCXNOW_DOMAIN+MCXNOW_ACTION["login"], data=logindata)
        if result==0:
            return MCXNOW_ERROR['HTTP Error']
        else:
            if result.status_code==200:
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                texthtml=result.text
                if 'sk' in texthtml :
                    self.User.SecretKey=texthtml.split('sk=')[1].split("'")[0]
                    self.Trading=True
                    return MCXNOW_ERROR['Ok']
                else :
                    return MCXNOW_ERROR['Unknown']
            else:
                return MCXNOW_ERROR['HTTP Error']

    def Login(self, username=None, password=None):
        #
        # Login : log to mcxnow.com
        #
        # Return 1 if success
        # if return 0
        # self.ErrorCode give you the error !
        #        
        self.Return=None
        if self.User.UserName==None and username==None:
            if self.User.Password==None and password==None:
                self.ErrorCode=MCXNOW_ERROR['Anonymous connexion']
                return 0
            else:
                self.ErrorCode=MCXNOW_ERROR['No UserName']
                return 0
        elif self.User.Password==None and password==None:
           self.ErrorCode=MCXNOW_ERROR['No Password']
           return 0
        else:
            if self.User.UserName==None:
                self.User.UserName=username
            if self.User.Password==None:
                self.User.Password=password
            self.ErrorCode=self.__Login__()
            if self.ErrorCode==1: # OK
                self.ErrorCode=self.__LoadUserDetails__()
                return 1
            else:
                return 0

    def __Logout__(self):
        self.Return=None
        result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["logout"]+"&sk="+self.User.SecretKey)
        if result==0:
            return MCXNOW_ERROR['HTTP Error']
        else:
            if result.status_code==200:
                texthtml=result.text
                if 'sk' in texthtml :
                    return MCXNOW_ERROR['Unknown']
                else :
                    self.User=McxNowUser()
                    return MCXNOW_ERROR['Ok']
            else:
                return MCXNOW_ERROR['HTTP Error']

    def Logout(self):
        #
        # Logout : logout from mcxnow.com
        #
        # Return 1 if success
        # if return 0
        # self.ErrorCode give you the error !
        #
        self.Return=None
        if self.Trading:
            self.ErrorCode=self.__Logout__()
            if self.ErrorCode==MCXNOW_ERROR['Ok']: # OK
                self.Trading=False
                return 1
            else:
                return 0
        else:
            self.ErrorCode=MCXNOW_ERROR['Already Disconnected']
            return 0

    def __CheckSecretKey__(self, texthtml):
        sk=""
        if 'sk' in texthtml :
            sk=texthtml.split('sk=')[1].split("'")[0]
        if self.User.SecretKey==sk:
            return 1
        else:
            return 0



    def __LoadUserDetails__(self):
        #
        # __LoadUserDetails__ : download all info about user account
        #
        # Account Info are in the variable User.Details
        #
        self.Return=None
        if self.Trading:
            result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
            if result==0:
                return MCXNOW_ERROR['HTTP Error']
            else:
                texthtml=result.text
                if self.__CheckSecretKey__(texthtml):
                    parser = UserAccountHTMLParser()
                    parser.feed(texthtml)
                    i=0
                    for cur in MCXNOW_ALLCURRENCY:
                        self.User.Details.Funds[cur].Balance=float(parser.data[3*i+1].split('Balance:')[1].split(cur)[0])
                        depositaddress=str(parser.data[3*i+2])
                        if depositaddress=='Get Deposit Address':
                            self.User.Details.Funds[cur].DepositAddress=''
                        else:
                            self.User.Details.Funds[cur].DepositAddress=depositaddress
                        self.User.Details.Funds[cur].MinimumDeposit=float(parser.deposit[6*i+1].split(cur)[0])
                        self.User.Details.Funds[cur].WithdrawFee=float(parser.deposit[6*i+3].split(cur)[0])
                        self.User.Details.Funds[cur].DepositConfirmations=int(parser.deposit[6*i+5])
                        self.User.Details.Funds[cur].Incoming=parser.incoming[cur]
                        i+=1
                    self.Return=self.User.Details
                    return MCXNOW_ERROR['Ok']
                else:
                    self.Trading=False
                    return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']

    def GetUserDetails(self):
        #
        # GetUserDetails : return a list with UserAccountInfo
        # each element is [$Currency$,$Balance$,$Incoming$,$DepositAddress$,$MinimumDeposit$,$DepositConfirmations$,$WithdrawFee$]
        #
        # Remarque : Account Info are in the variable User.Details of the class.
        #
        # if return [], then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadUserDetails__()
        if self.ErrorCode==MCXNOW_ERROR['Ok']: #OK
            result=[]
            for cur in MCXNOW_ALLCURRENCY:
                result.append(self.User.Details.GetInfo(cur))
            return result
        else:
            return []
        
    def GetUserAccountInfo(self, cur):
        #
        # GetUserAccountInfo : return a list 
        # [$Currency$,$Balance$,$Incoming$,$DepositAddress$,$MinimumDeposit$,$DepositConfirmations$,$WithdrawFee$]
        #
        # Remarque : Account Info Currency are in the variable User.Details.Funds[$currency$] of the class.
        #
        # if return [], then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadUserDetails__()
        if self.ErrorCode==MCXNOW_ERROR['Ok']: #OK
            if cur in MCXNOW_ALLCURRENCY:
                return self.User.Details.GetInfo(cur)
            else:
                self.ErrorCode=MCXNOW_ERROR['Unknown Currency']
                return []
        else:
            return []

    def __LoadUserOrders__(self, cur, skchecked=False):
        #
        # __LoadUserOrders__ : download user all orders for a specific currency
        #
        # Orders are in the variable User.Book.Orders[$currency$]
        #
        self.Return=None        
        if self.Trading:
            if not(skchecked):
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                if result==0:
                    return MCXNOW_ERROR['HTTP Error']
                else:                
                    texthtml=result.text
                    if self.__CheckSecretKey__(texthtml):
                        skOk=True
                    else:
                        skOk=False
            else:
                skOk=True
            if skOk:
                if cur in MCXNOW_TRADEDCURRENCY:
                    result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["info"]+"cur="+cur)
                    if result==0:
                        return MCXNOW_ERROR['HTTP Error']
                    else:                
                        textxml=result.text
                        if ('<orders>')in textxml:
                            orderslist=textxml.split('<orders>')[1].split('</orders>')[0]
                            orders=orderslist.split('<o>')
                            self.User.Book.ClearCurrencyAllOrders(cur)
                            for i in range(1,len(orders)):
                                order_id=int(orders[i].split('<id>')[1].split('</id>')[0])
                                order_confirm=int(orders[i].split('<e>')[1].split('</e>')[0])
                                order_time=int(orders[i].split('<t>')[1].split('</t>')[0])#time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(orders[i].split('<t>')[1].split('</t>')[0])))
                                order_type=int(orders[i].split('<b>')[1].split('</b>')[0])
                                order_amount=float(orders[i].split('<a1>')[1].split('</a1>')[0])
                                order_price=float(orders[i].split('<p>')[1].split('</p>')[0])
                                self.User.Book.AddOrder(cur, order_id,  order_type,order_time, order_confirm, order_amount, order_price)
                        else:
                            return MCXNOW_ERROR['HTTP Error']
                        if ('<base_bal>')in textxml:
                            base_bal=float(textxml.split('<base_bal>')[1].split('</base_bal>')[0])
                            self.User.Book.AddBaseBalance(cur, base_bal)
                        else:
                            return MCXNOW_ERROR['HTTP Error']
                        if ('<cur_bal>')in textxml:
                            cur_bal=float(textxml.split('<cur_bal>')[1].split('</cur_bal>')[0])
                            self.User.Book.AddCurrencyBalance(cur, cur_bal)
                        else:
                            return MCXNOW_ERROR['HTTP Error']
                        self.Return=self.User.Book.Orders[cur]
                        return MCXNOW_ERROR['Ok']
                else:
                    return MCXNOW_ERROR['Unknown Currency']                    
            else:
                self.Trading=False
                return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']


    def __LoadUserAllOrders__(self):
        #
        # __LoadUserAllOrders__ : download user all orders for all currency
        #
        # Orders are in the variable User.Book
        #
        self.Return=None        
        if self.Trading:
            result=request(self.Session,'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
            if result==0:
                return MCXNOW_ERROR['HTTP Error']
            else:    
                texthtml=result.text
                if self.__CheckSecretKey__(texthtml):
                    for cur in MCXNOW_TRADEDCURRENCY:
                        self.__LoadUserOrders__(cur, True)
                    self.Return=self.User.Book
                    return MCXNOW_ERROR['Ok']
                else:
                    self.Trading=False
                    return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']

    def GetUserOrders(self, cur):
        #
        # GetUserOrders : return a list with User Orders for the currency cur
        # each element is [$Id$,$Type$,,$Time$,$Confirmed$,$Amount$,Price$]
        # or [None] if no orders
        #
        # Remarque : Users Currency Orders are in the variable User.Book.Orders[$currency$] of the class.
        # 
        #
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadUserOrders__(cur)
        if self.ErrorCode==MCXNOW_ERROR['Ok']: 
            if cur in MCXNOW_ALLCURRENCY:
                if self.User.Book.Orders[cur]==None:
                    return [None]
                else:
                    result=[]
                    for Id in self.User.Book.Orders[cur].Id:
                        result.append([Id, self.User.Book.Orders[cur].Id[Id].Type, self.User.Book.Orders[cur].Id[Id].Time, self.User.Book.Orders[cur].Id[Id].Confirmed, self.User.Book.Orders[cur].Id[Id].Amount, self.User.Book.Orders[cur].Id[Id].Price])
                    return result
            else:
                self.ErrorCode=MCXNOW_ERROR['Unknown Currency']
                return []
        else:
            return []        
            
    def GetUserAllOrders(self):
        #
        # GetUserAllOrders : return a list with All User Orders
        # each element is a list : 
        # [$currency$,[$Order1$,$Order2$,...] where $Orderi$ is [$Id$,$Type$,,$Time$,$Confirmed$,$Amount$,Price$]
        # or [None] if no orders
        #
        # Remarque : Users All Orders are in the variable User.Book of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadUserAllOrders__()
        if self.ErrorCode==1: #OK
            result=[]
            for cur in MCXNOW_TRADEDCURRENCY:
                if self.User.Book.Orders[cur]==None:
                    result.append([cur, [None]])
                else:
                    resultorders=[]
                    for Id in self.User.Book.Orders[cur].Id:
                        resultorders.append([Id, self.User.Book.Orders[cur].Id[Id].Type, self.User.Book.Orders[cur].Id[Id].Time, self.User.Book.Orders[cur].Id[Id].Confirmed, self.User.Book.Orders[cur].Id[Id].Amount, self.User.Book.Orders[cur].Id[Id].Price])
                    result.append([cur, resultorders])
            return result
        else:
            return []        
            
        


    def __LoadCurrencyInfo__(self, cur):
        #
        # __LoadCurrencyInfo__ : download for a specific currency
        # 1) Book orders 
        # 2) History trading
        # 3) Info : Users logged - Volume - Last price - Low and High price
        #
        # Orders are in two variables Public.BookBuy.Orders[$currency$] and Public.BookSell.Orders[$currency$]
        # History are in the variable Public.History.Orders[$currency$]
        # Users Logged info is in the variable Public.UsersLogged
        # Info are in the variable Public.Info[$currency$]
        #
        self.Return=None         
        if cur in MCXNOW_TRADEDCURRENCY:
            result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["ordersbook"]+"cur="+cur)
            if result==0:
                return MCXNOW_ERROR['HTTP Error']
            else:
                textxml=result.text
                if '<buy>' in textxml:
                    buyorders=textxml.split('<buy>')[1].split('</buy>')[0]
                    sellorders=textxml.split('<sell>')[1].split('</sell>')[0]
                    historyorders=textxml.split('<history>')[1].split('</history>')[0]
                    volumeorders=textxml.split('<vol>')[1].split('</vol>')[0]
                    users=int(textxml.split('<users>')[1].split('</users>')[0])
                    curvol=float(textxml.split('<curvol>')[1].split('</curvol>')[0])
                    basevol=float(textxml.split('<basevol>')[1].split('</basevol>')[0])
                    lastprice=float(textxml.split('<lprice>')[1].split('</lprice>')[0])
                    lowprice=float(textxml.split('<pricel>')[1].split('</pricel>')[0])
                    highprice=float(textxml.split('<priceh>')[1].split('</priceh>')[0])
                    # volumeorders // TODO
                    self.Public.Info.Add(cur, curvol, basevol, lastprice, lowprice, highprice)
                    self.Public.UsersLogged=users
                    # Buy Orders
                    orders=buyorders.split('<o>')
                    self.Public.BookBuy.ClearOrders(cur)
                    for i in range(1,len(orders)-1):
                        order_price=float(orders[i].split('<p>')[1].split('</p>')[0])
                        order_amount=float(orders[i].split('<c1>')[1].split('</c1>')[0])
                        order_amountBTC=float(orders[i].split('<c2>')[1].split('</c2>')[0])
                        self.Public.BookBuy.AddOrder(cur, 'Sell', order_price, order_amount, order_amountBTC )
                    # Sell Orders
                    orders=sellorders.split('<o>')
                    self.Public.BookSell.ClearOrders(cur)
                    for i in range(1,len(orders)-1):
                        order_price=float(orders[i].split('<p>')[1].split('</p>')[0])
                        order_amount=float(orders[i].split('<c1>')[1].split('</c1>')[0])
                        order_amountBTC=float(orders[i].split('<c2>')[1].split('</c2>')[0])
                        self.Public.BookSell.AddOrder(cur, 'Sell', order_price, order_amount, order_amountBTC )
                    # History Orders
                    orders=historyorders.split('<o>')
                    self.Public.History.ClearOrders(cur)
                    for i in range(1,len(orders)):
                        order_time=int(orders[i].split('<t>')[1].split('</t>')[0])#time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(orders[i].split('<t>')[1].split('</t>')[0])))
                        order_type=int(orders[i].split('<b>')[1].split('</b>')[0])
                        #if int(orders[i].split('<b>')[1].split('</b>')[0])==1:
                        #    order_type="Buy"
                        #else:
                        #    order_type="Sell"
                        order_price=float(orders[i].split('<p>')[1].split('</p>')[0])
                        order_amount=float(orders[i].split('<c1>')[1].split('</c1>')[0])
                        order_amountBTC=float(orders[i].split('<c2>')[1].split('</c2>')[0])
                        self.Public.History.AddOrder(cur, order_time,order_type, order_price, order_amount, order_amountBTC )
                    self.Return=self.Public
                    return MCXNOW_ERROR['Ok']
                else:
                    return MCXNOW_ERROR['Unknown']

    def GetCurrencyBookOrders(self, cur):
        #
        # GetCurrencyBookOrders : return a list with BookOrders for the currency cur
        # each element is a pair [$buy$,$sell$]
        # where $buy$ et $sell$ are order in format [$Price$,$Amout$,$AmountBTC$]
        #
        # Remarque : CurrencyBookOrders are in the two variables Public.BookBuy.Orders[$currency$] and Public.BookSell.Orders[$currency$] of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadCurrencyInfo__(cur)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            if cur in MCXNOW_TRADEDCURRENCY:
                i=0
                result=[]
                while (i<len(self.Public.BookBuy.Orders[cur].Id) )or (i<len(self.Public.BookSell.Orders[cur].Id)):
                    if (i<len(self.Public.BookBuy.Orders[cur].Id)):
                        buyorder=[self.Public.BookBuy.Orders[cur].Id[i].Price, self.Public.BookBuy.Orders[cur].Id[i].Amount, self.Public.BookBuy.Orders[cur].Id[i].AmountBTC]
                    else:
                        buyorder=None
                    if (i<len(self.Public.BookSell.Orders[cur].Id)):
                        sellorder=[self.Public.BookSell.Orders[cur].Id[i].Price, self.Public.BookSell.Orders[cur].Id[i].Amount, self.Public.BookSell.Orders[cur].Id[i].AmountBTC]
                    else:
                        sellorder=None
                    result.append([buyorder, sellorder])
                    i+=1
                return result
            else:
                self.ErrorCode=MCXNOW_ERROR['Unknown Currency']
                return []
        else:
            return []        

    def GetCurrencyHistoryOrders(self, cur):
        #
        # GetCurrencyHistoryOrders : return a list with HistoryOrders for the currency cur
        # each element is a order in format [$Time$,$Type$,$Amou$,$AmountBTC$,$Price$]
        #
        # Remarque : CurrencyHistoryOrders are in the variable Public.History.Orders[$currency$] of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadCurrencyInfo__(cur)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            if cur in MCXNOW_TRADEDCURRENCY:
                i=0
                result=[]
                while (i<len(self.Public.History.Orders[cur].Id) ):
                    result.append([self.Public.History.Orders[cur].Id[i].Time, self.Public.History.Orders[cur].Id[i].Type, self.Public.History.Orders[cur].Id[i].Amount, self.Public.History.Orders[cur].Id[i].AmountBTC, self.Public.History.Orders[cur].Id[i].Price])
                    i+=1
                return result
            else:
                self.ErrorCode=MCXNOW_ERROR['Unknown Currency']
                return []
        else:
            return []        

    def GetCurrencyInfo(self, cur):
        #
        # GetCurrencyInfo : return a list with Info for the currency cur
        # each element is a order in format [$Volume$,$VolumeBTC$,$LastPrice$,$PriceLow$,$PriceHigh$]
        #
        # Remarque : CurrencyInfo is in the variable Public.Info.Currency[$currency$] of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadCurrencyInfo__(cur)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            if cur in MCXNOW_TRADEDCURRENCY:
                return self.Public.Info.Currency[cur].GetInfo()
            else:
                self.ErrorCode=MCXNOW_ERROR['Unknown Currency']
                return []
        else:
            return []
        
    def GetAllCurrencyInfo(self):
        #
        # GetAllCurrencyInfo : return a list with Info for all currency
        # each element is a info in format $Currency$,[$Volume$,$VolumeBTC$,$LastPrice$,$PriceLow$,$PriceHigh$]
        #
        # Remarque : Info is in the variable Public.Info.Currency of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        result=[]
        for cur in MCXNOW_TRADEDCURRENCY:
            self.ErrorCode=self.__LoadCurrencyInfo__(cur)
            if self.ErrorCode==MCXNOW_ERROR['Ok']:
                result.append([cur, self.Public.Info.Currency[cur].GetInfo()])
            else:
                result.append([cur, None])
        self.ErrorCode=MCXNOW_ERROR['Ok']
        return result
    


    def __LoadAllCurrencyInfo__(self):
        #
        # __LoadAllCurrencyInfo__ : download for all currency
        # 1) Book orders 
        # 2) History trading
        # 3) Info : users logged - Volume - Last price - Low and High price
        #
        # Orders are in two variables Public.BookBuy.Orders and Public.BookSell.Orders
        # History are in the variable Public.History
        # Users Logged info is in the variable Public.UsersLogged
        # Info are in the variable Public.Info
        #
        for cur in MCXNOW_TRADEDCURRENCY:
            self.__LoadCurrencyInfo__(cur)


    def __SendAOrder__(self, cur=None, type=None, amt=0, price=0, confirm=0, skchecked=False):
        #
        # SendOrder : send a order
        #
        self.Return=None            
        if self.Trading:
            if not(skchecked):
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                if result==0:
                    return MCXNOW_ERROR['HTTP Error']
                else:                
                    texthtml=result.text
                    if self.__CheckSecretKey__(texthtml):
                        skOk=True
                    else:
                        skOk=False
            else:
                skOk=True
            if skOk:        
                if cur in MCXNOW_TRADEDCURRENCY:
                    self.__LoadUserOrders__(cur, True)
                    base_bal=self.User.Book.BaseBalance[cur]
                    cur_bal=self.User.Book.CurrencyBalance[cur]
                    amt=self.__parseFloat__(amt)
                    price=self.__parseFloat__(price)
                    #if type=='Sell':
                    if (amt>cur_bal and type==0) or (amt>base_bal and type==1):
                        return MCXNOW_ERROR['Trade Error No Enough Coins']
                    elif (amt<0.2 and type ==0) or (amt<0.01 and type==1):
                        return MCXNOW_ERROR['Trade Error Minimum Request']
                    elif price<0.00000001:
                        return MCXNOW_ERROR['Trade Error Price below minimum']
                    elif confirm==0 or confirm==1:
                        if self.User.Book.Orders[cur]==None:
                            l=0
                            IdList=[]
                        else :
                            l=len(self.User.Book.Orders[cur].Id)
                            IdList=self.User.Book.Orders[cur].GetId()
                        if l<10:
                            result=request(self.Session, 'get',MCXNOW_DOMAIN+MCXNOW_ACTION["trade"]+"&cur="+cur+"&sk="+self.User.SecretKey+'&amt='+str(amt)+'&price='+str(price)+'&buy='+str(type)+'&enabled=0')#+str(confirm))
                            if result==0:
                                return MCXNOW_ERROR['HTTP Error']
                            else:                                
                                self.__LoadUserOrders__(cur, True)
                                if len(self.User.Book.Orders[cur].Id)==l+1: #success
                                    IdNewList=self.User.Book.Orders[cur].GetId()
                                    for id in IdNewList:
                                        if id not in IdList:
                                            tmpReturn=self.User.Book.Orders[cur].GetOrderInfo(id)
                                            if confirm==1:
                                                self.__ExecuteOrder__(cur, id, True)
                                                tmpReturn[0]=None
                                            self.Return=tmpReturn
                                            return MCXNOW_ERROR['Ok']
                                else:
                                    return MCXNOW_ERROR['Trade Error Order not send']
                        else:
                            return MCXNOW_ERROR['Trade Error Ten Order already']
                    else:
                        return MCXNOW_ERROR['Trade Error Confirm']
                else:
                    return MCXNOW_ERROR['Trade Error Currency not accepted']
            else:
                self.Trading=False
                return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']


    def SendSellOrder(self, cur=None, amt=0, price=0 , confirm=0):
        #
        # SendSellOrder : send a sell order 
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # if confirm=0:
        #       self.Return=[$id$,0,$time$,$amt$,$price$] 
        # else : 
        #       self.Return=[None,0,$time$,$amt$,$price$] (because this order can be executed yet)
        # 
        if self.Trading:
            result=request(self.Session,'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
            if result==0:
                self.ErrorCode=MCXNOW_ERROR['HTTP Error']
                return 0
            else:             
                texthtml=result.text
                if self.__CheckSecretKey__(texthtml):
                    self.ErrorCode=self.__SendAOrder__(cur, 0, amt, price, confirm, True)
                    if self.ErrorCode==1:
                        return 1
                    else:
                        return 0
                else:
                    self.ErrorCode=MCXNOW_ERROR['Session ended']
                    return 0
        else:
            self.ErrorCode=MCXNOW_ERROR['Anonymous connexion']
            return 0

    def SendBuyOrder(self, cur=None, amt=0, price=0 , confirm=0):
        #
        # SendBuyOrder : send a buy order 
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # if confirm=0:
        #       self.Return=[$id$,1,$time$,$amt$,$price$] 
        # else : 
        #       self.Return=[None,1,$time$,$amt$,$price$] (because this order can be executed yet)
        # # 
        
        if self.Trading:
            result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
            if result==0:
                self.ErrorCode=MCXNOW_ERROR['HTTP Error']
                return 0            
            else:
                texthtml=result.text
                if self.__CheckSecretKey__(texthtml):
                    self.ErrorCode=self.__SendAOrder__(cur, 1,  amt, price, confirm, True)
                    if self.ErrorCode==1:
                        return 1
                    else:
                        return 0
                else:
                    self.ErrorCode=MCXNOW_ERROR['Session ended']
                    return 0
        else:
            self.ErrorCode=MCXNOW_ERROR['Anonymous connexion']
            return 0

    def __ExecuteOrder__(self, cur, id, skchecked=False):
        #
        # ExecuteOrder : execute a order to confirm
        # 
        self.Return=None
        if self.Trading:
            if not(skchecked):
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                if result==0:
                    return MCXNOW_ERROR['HTTP Error']
                else:                
                    texthtml=result.text
                    if self.__CheckSecretKey__(texthtml):
                        skOk=True
                    else:
                        skOk=False
            else:
                skOk=True
            if skOk:
                self.__LoadUserOrders__(cur, True)
                if self.User.Book.Orders[cur]<>None:
                    if id in self.User.Book.Orders[cur].Id:
                        if self.User.Book.Orders[cur].Id[id].Confirmed:
                            self.Return=None
                            return MCXNOW_ERROR['Confirm Error Already Confirmed']
                        else:
                            self.Return=self.User.Book.Orders[cur].GetOrderInfo(id)
                            self.Session.get(MCXNOW_DOMAIN+MCXNOW_ACTION["exectrade"]+"&sk="+self.User.SecretKey+"&cur="+cur+'&id='+str(id))
                            return MCXNOW_ERROR['Ok']
                    else:
                        self.Return=None
                        return MCXNOW_ERROR['Confirm Error No order with this id']
                else:
                    self.Return=None
                    return MCXNOW_ERROR['Confirm Error No order with this id']
            else:
                self.Trading=False
                return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']
    
    def ExecuteOrder(self, cur, id):
        #
        # ExecuteOrder : execute a order to confirm
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=[None,$type$,$time$,$amt$,$price$]  (order info)
        self.ErrorCode=self.__ExecuteOrder__(cur, id)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            self.Return[0]=None
            return 1
        else:
            return 0
        
    def __CancelOrder__(self, cur, id, skchecked=False):
        #
        #CancelOrder : cancel a order
        #
        self.Return=None
        if self.Trading:
            if not(skchecked):
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                if result==0:
                    return MCXNOW_ERROR['HTTP Error']
                else:                
                    texthtml=result.text
                    if self.__CheckSecretKey__(texthtml):
                        skOk=True
                    else:
                        skOk=False
            else:
                skOk=True
            if skOk:
                self.__LoadUserOrders__(cur, True)
                if self.User.Book.Orders[cur]<>None:
                    if id in self.User.Book.Orders[cur].Id:
                        self.Return=self.User.Book.Orders[cur].GetOrderInfo(id)
                        self.Session.get(MCXNOW_DOMAIN+MCXNOW_ACTION["canceltrade"]+"&sk="+self.User.SecretKey+"&cur="+cur+'&id='+str(id))
                        return MCXNOW_ERROR['Ok']
                    else:
                        self.Return=None
                        return MCXNOW_ERROR['Confirm Error No order with this id']
                else:
                    self.Return=None
                    return MCXNOW_ERROR['Confirm Error No order with this id']
            else:
                self.Trading=False
                return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']
            
    def CancelOrder(self, cur, id):
        #
        # CancelOrder : cancel a order
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=[None,$type$,$time$,$amt$,$price$]  (order info)
        self.ErrorCode=self.__CancelOrder__(cur, id)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            self.Return[0]=None
            return 1
        else:
            return 0

    def __CancelAllOrders__(self, cur):
        #
        #CancelAllOrders : cancel all orders of one currency
        #
        self.Return=None
        if self.Trading:
            result=self.Session.get(MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
            if result==0:
                return MCXNOW_ERROR['HTTP Error']
            else:              
                texthtml=result.text
                if self.__CheckSecretKey__(texthtml):
                    self.__LoadUserOrders__(cur, True)
                    if self.User.Book.Orders[cur]==None:
                        return MCXNOW_ERROR['Ok']
                    else:
                        for id in self.User.Book.Orders[cur].Id:
                            self.CancelOrder(cur, id)
                        return MCXNOW_ERROR['Ok']
                else:
                    self.Trading=False
                    return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']

    def CancelAllOrders(self, cur):
        #
        # CancelAllOrders : cancel all orders of one currency
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        self.ErrorCode=__CancelOrder__(cur)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            return 1
        else:
            return 0


    def __LoadChat__(self):
        #
        # __LoadChat__ : download all chat
        #
        # All Message are in the liste Public.Chat
        #
        self.Return=None         
        result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["chat"])
        if result==0:
            return MCXNOW_ERROR['HTTP Error']
        else:
            textxml=result.text
            if '<doc>' in textxml:
                # Messages
                self.Public.Chat.ClearChat()
                messages=textxml.split('<c>')
                for i in range(1, len(messages)):
                    message_user=messages[i].split('<n>')[1].split('</n>')[0]
                    message_id=messages[i].split('<i>')[1].split('</i>')[0]
                    message_text=messages[i].split('<t>')[1].split('</t>')[0]
                    self.Public.Chat.AddMessage(message_id, message_user, message_text)
                self.Return=self.Public
                return MCXNOW_ERROR['Ok']
            else:
                return MCXNOW_ERROR['Unknown']                

    def GetChat(self):
        #
        # GetChat : return a list with Message in chat
        # each element is [$Id$,$User$,$Messsage$]
        # or [] if no chat  (?!?)
        #
        # Remarque : Chat is in the variable User.Public.Chat of the class.
        # 
        #
        # if return [] then self.ErrorCode give you the errorcode !
        #
        self.ErrorCode=self.__LoadChat__()
        if self.ErrorCode==1:
            result=[]
            for i in range(len(self.Public.Chat.Message)):
                result.append([self.Public.Chat.Message[i].Id, self.Public.Chat.Message[i].User, self.Public.Chat.Message[i].Text])
            return result
        else:
            return[]


    def __SendChatMsg__(self, msg, skchecked=False):
        #
        # __SendChatMsg__ : Send a message $msg$ to chat
        # 
        self.Return=None
        if self.Trading:
            if not(skchecked):
                result=request(self.Session, 'get', MCXNOW_DOMAIN+MCXNOW_ACTION["useraccount"])
                if result==0:
                    return MCXNOW_ERROR['HTTP Error']
                else:                
                    texthtml=result.text
                    if self.__CheckSecretKey__(texthtml):
                        skOk=True
                    else:
                        skOk=False
            else:
                skOk=True
            if skOk:
                self.Session.get(MCXNOW_DOMAIN+MCXNOW_ACTION["sendchat"]+"&sk="+self.User.SecretKey+"&t="+str(msg))
                return MCXNOW_ERROR['Ok']
            else:
                self.Trading=False
                return MCXNOW_ERROR['Session ended']
        else:
            return MCXNOW_ERROR['Anonymous connexion']


    def SendChatMsg(self, msg):
        #
        # SendChatMsg : Send the $msg$ to chat
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=$msg$
        self.ErrorCode=self.__SendChatMsg__(msg)
        if self.ErrorCode==MCXNOW_ERROR['Ok']:
            self.Return=str(msg)
            return 1
        else:
            return 0
            
