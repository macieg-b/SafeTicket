from flask import Response
from setting import hostData, userData, passData, dbData
import MySQLdb
from math import fabs
from datetime import datetime, timedelta

def checkBalance(email):
    db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
    cur = db.cursor()
    cur.execute("SELECT `Balance` FROM `USERS` WHERE `Login` = %s", [email])
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
    #Catch data from jsonArg
    email = jsonArg['email']
    cityName = jsonArg['cityname']
    discount = jsonArg['discount']
    typ = jsonArg['type']
    time = jsonArg['time']
    count = jsonArg['count']
    price = jsonArg['price']

    #User doesn't exsist in DB
    if checkBalance(email)==None:
        return Response(status=203)
    #User exsist in DB
    else:
        balance = checkBalance(email)
        priceSum = float(price) * float(count)
        #Not enough funds
        if priceSum>balance:
            return Response(status=202)
        #Enough funds
        else:
            db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
            db.autocommit(False)
            cur = db.cursor()
            newBalance = balance - fabs(priceSum)
            starttime = datetime.utcnow() + timedelta(hours=2)
            try:
                cur.execute("INSERT INTO `tickets` (`email`, `cityname`, `discount`, `type`, `time`, `count`, `price`, `starttime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [email, cityName, discount, typ, time, count, price, starttime])
                cur.execute("UPDATE `USERS` SET `balance`=%s WHERE `Login`=%s", [newBalance, email])
                db.commit()
                return Response(status=200)
            except ValueError:
                print ValueError
                db.rollback()
                return Response(status=206)
