from setting import hostData, userData, passData, dbData
import MySQLdb
def SelectAll():
    print "TEST"
    db = MySQLdb.connect(host = hostData, user = userData, passwd = passData, db = dbData)
    cur = db.cursor()

    cur.execute("SELECT * FROM `USERS`")
    result = cur.fetchall()
    print result
    cur.close()
    db.close()
    return result
