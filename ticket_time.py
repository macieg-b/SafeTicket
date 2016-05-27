from flask import Response
from setting import hostData, userData, passData, dbData
import MySQLdb

def checkBalance(email):
    db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
    cur = db.cursor()
    cur.execute("SELECT `balance` FROM `USERS` WHERE `Login` = %s", (email))
    result = cur.fetchall()

    if (cur.rowcount == 0):
        cur.close()
        db.close()
        return None
    else:
        for row in result:
            balance=row[0]
        cur.close()
        db.close()
        return balance

def buyTickets(jsonArg):
    print "W time ticket"
    priceSum=jsonArg['price']*jsronArg['count']
    if(checkBalance(jsonArg['email']) == None):
        return Response(type=403)
    else:
        balance=checkBalance(jsonArg['email'])

    if(priceSum>balance):
        return Response(type=202)
    else:
        newBalance=balance-priceSum
        db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
        cur = db.cursor()
        cur.execute("INSERT INTO `tickets` (`email`, `cityname`, `discount`, `type`, `time`, `count`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (jsonArg['email'], jsonArg['cityname'], jsonArg['discount'], jsonArg['type'], jsonArg['time'], jsonArg['count'], jsonArg['price']))
        cur.execute("UPDATE `USERS` SET `balance`=%s WHERE `Login`=%s", (newBalance, jsonArg['email']))
        db.commit()
        cur.close()
        db.close()
        return Response(type=200)
