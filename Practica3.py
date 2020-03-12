from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import mysql.connector as mysql

while(1):
    e=""
    i=0
    con=mysql.connect(host='localhost',user='root',passwd='',db='datos')
    operacion=con.cursor()
    operacion.execute("SELECT * FROM web;")
    for enlace,estatus in operacion.fetchall():
        print(enlace+" "+str(estatus))
        if(estatus==0):
            try:
                url=urlopen(enlace)
            except urllib.error.HTTPError:
                continue
            except UnicodeEncodeError:
                continue
            bs=BeautifulSoup(url.read(),'html.parser',from_encoding="iso-8859-1")
            for enlaces in bs.find_all("a"):
                s=enlaces.get("href")
                try:
                    if(s[0:4]=="http"):
                        try:
                            operacion.execute("insert into web values('"+s+"',0);")
                            print(s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                    else:
                        try:
                            operacion.execute("insert into web values('"+enlace+s+"',0);")
                            print(enlace+s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                except TypeError:
                    pass
            i=1
            operacion.execute("update web set estatus=1 where enlace='"+enlace+"';")

            con.commit()

    con.close()
    if(i==0):
        break