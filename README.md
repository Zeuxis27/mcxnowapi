mcxnowapi (Version 1.0)
==================

This library provides some method to access at the fuctionnality of mcXnow.com crypto exchange market.
You can develop your one application based on this Api with Python 2.7 (bot, gui,...).

Installation:
-----------

    just the cmd :      python setup.py install
    
Module needed :
--------------

    You need the module requests : http://docs.python-requests.org
    
    
For the samples, pyqt4 and mathplotlib


NOTE: mcxnow is not affiliated with this project; this is a completely independent implementation based on the API description. Use at your own risk.


Donations :
----------

If you find the library useful and would like to donate please send some coins here:

 * BTC : 18ZqmXd8xzUtzAhDXZwBJQgyHV8Rxo7GV1
 * LTC : LVjfq1JNvCX2qHLxTzQoEfRnh4EbdZui51
 * MNC : MA6RGr42cioJsCkAYLt8kV5sxjiNfDh6si
 * SC : sJwUHidU7x5o7kDDxPjXVKbYq3EpLca1iV
 * WDC : Wk4j5PGzUWvm311H6TPcQwK3pzNMZknPjS
 * FTC : 6zVjFJNJwBN3u6esi6uW54z3vY8L3hemCv
 
 
Any question, suggestion or help please send a mail to : zeuxis27@gmail.com



If you dev something with this api, think about my contribution....

I you see error... please give me a sign !

ENJOY ;-)


Documentation :
--------------

The main class is McxNowSession.

You can use her for :
1) Anonymous session or 2) User session.

Class use :

* S=McxNowSession() : open a anonymous session and give you access to all data from mcxnow but you can trade.
    
* S=McxNowSession(username,password) : open a user session and give you access to all public data AND your account : you can trade !!!
    
    

The variables are :
* S.User : class with all user info
* S.Public : class with all public info
* S.ErrorCode : error code (see at bottom the code) returned by a methfunction
* S.Return : after a methfunction call, contain the class or variable returned by the methfunction
* S.Trading : True if User Session else False

The methfunctions are :

+ Anonymous and user sessions :

>S.GetCurrencyBookOrders(cur) :

    return a list with BookOrders for the currency cur
        # each element is a pair [$buy$,$sell$]
        # where $buy$ and $sell$ are order in format [$Price$,$Amout$,$AmountBTC$]
        #
        # Remarque : CurrencyBookOrders is in the two variables S.Public.BookBuy.Orders[$currency$] 
        # and S.Public.BookSell.Orders[$currency$] of the class.
        # 
        # if return [] then S.ErrorCode give you the errorcode !
        #

>S.GetCurrencyHistoryOrders(cur) : 

    return a list with HistoryOrders for the currency cur
        # each element is a order in format [$Time$,$Type$,$Amout$,$AmountBTC$,$Price$]
        #
        # Remarque : CurrencyHistoryOrders is in the variable S.Public.History.Orders[$currency$] of the class.
        # 
        # if return [] then S.ErrorCode give you the errorcode !
        #
        
>S.GetCurrencyInfo(cur) :

    return a list with Info for the currency cur
        # each element is a order in format [$Volume$,$VolumeBTC$,$LastPrice$,$PriceLow$,$PriceHigh$]
        #
        # Remarque : CurrencyInfo is in the variable S.Public.Info.Currency[$currency$] of the class.
        # 
        # if return [] then S.ErrorCode give you the errorcode !
        #        

>S.GetAllCurrencyInfo() : 

    return a list with Info for all currency
        # each element is a info in format $Currency$,[$Volume$,$VolumeBTC$,$LastPrice$,$PriceLow$,$PriceHigh$]
        #
        # Remarque : Info is in the variable Public.Info of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        
>S.GetChat() : 

    return a list with Message in chat
        # each element is [$Id$,$User$,$Messsage$]
        # or [] if no chat  (?!?)
        #
        # Remarque : Chat is in the variable User.Public.Chat of the class.
        # 
        #
        # if return [] then self.ErrorCode give you the errorcode !
        #

        
        
+ User Session :

>S.Login(username,password)

    login to mcxnow.com if you have open a anonymous session or you have been disconnected
    
        #
        # Return 1 if success
        #
        # if return 0 : self.ErrorCode give you the error !
        #
    
>S.Logout()

    logout from mcxnow.com
        #
        # Return 1 if success
        #
        # if return 0 : self.ErrorCode give you the error !
        #
        
>S.GetUserDetails() : 

    return a list with UserAccountInfo
        # each element is 
        # [$Currency$,$Balance$,$Incoming$,$DepositAddress$,$MinimumDeposit$,$DepositConfirmations$,$WithdrawFee$]
        #
        # Remarque : Account Info are in the variable User.Details of the class.
        #
        # if return [], then self.ErrorCode give you the errorcode !
        #
        
>S.GetUserAccountInfo(cur) :

    return the list 
    [$Currency$,$Balance$,$Incoming$,$DepositAddress$,$MinimumDeposit$,$DepositConfirmations$,$WithdrawFee$]
        #
        # Remarque : Account Info Currency are in the variable User.Details.Funds[$currency$] of the class.
        #
        # if return [], then self.ErrorCode give you the errorcode !
        #
        
>S.GetUserOrders(cur) : 

    return a list with User Orders for the currency cur
        # each element is [$Id$,$Type$,$Time$,$Confirmed$,$Amount$,Price$]
        # or [None] if no orders
        #
        # Remarque : Users Currency Orders are in the variable User.Book.Orders[$currency$] of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        
>S.GetUserAllOrders() :

        return a list with All User Orders
        # each element is a list : 
        # [$currency$,[$Order1$,$Order2$,...]] where $OrderX$ is [$Id$,$Type$,,$Time$,$Confirmed$,$Amount$,Price$]
        # or [None] if no orders
        #
        # Remarque : Users All Orders are in the variable User.Book of the class.
        # 
        # if return [] then self.ErrorCode give you the errorcode !
        #
        
>S.SendSellOrder(cur, amt, price, confirm):

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
        
>S.SendBuyOrder(cur amt, price, confirm):

        #
        # SendBuyOrder : send a buy order 
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # if confirm=0:
        #       self.Return=[$id$,1,$time$,$amt$,$price$] 
        # else : 
        #       self.Return=[None,1,$time$,$amt$,$price$] (because this order can be executed yet)
        #
        
>>S.ExecuteOrder(cur, id):

        #
        # ExecuteOrder : execute the order id (to confirm)
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=[None,$type$,$time$,$amt$,$price$]  (order info)

>S.CancelOrder(cur,id) : 

        #
        # cancel the order id
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=[None,$type$,$time$,$amt$,$price$]  (order info)
        
>S.CancelAllOrders(cur) : 

        # cancel all orders of one currency
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        #
        
>>S.SendChatMsg(msg) :

        # Send the $msg$ to chat
        # Return 1 if success or 0 if error
        # 
        # if return 0 then self.ErrorCode give you the errorcode !
        # 
        #       self.Return=$msg$
        
+ ERROR CODE :

        Unknown : 0
        Ok : 1
        No UserName : 101
        No Password : 102
        Session ended :110
        Anonymous connexion :1000
        Already Disconnected : 1100
        Unknown Currency :2000
        HTTP Error :10000
        Trade Error No Enough Coins : 20000
        Trade Error Minimum Request : 20001 
        Trade Error Price below minimum : 20002
        Trade Error Order not send : 20003
        Trade Error Ten Order already : 20004
        Trade Error Type Error : 20005
        Trade Error Currency not accepted : 20006
        Trade Error Confirm : 20007
        Confirm Error Already Confirmed : 30001
        Confirm Error No order with this id : 30002
