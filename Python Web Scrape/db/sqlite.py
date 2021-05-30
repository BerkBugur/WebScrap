import sqlite3

con = sqlite3.connect("deneme.db")

cursor = con.cursor()

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satıcı TEXT, fiyat TEXT, resim TEXT)")


def degerEkle():
    cursor.execute("INSERT INTO urunler VALUES('Berk','Bugur','100','resim')")
    cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)", ('Burak','Bugur','200','resim2'))
    con.commit()
    con.close()

tabloolustur()
degerEkle()