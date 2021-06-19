

from mysql.connector import MySQLConnection, Error
import mysql.connector
from mysql.connector import errorcode
from datetime import date



config = {
    'user': 'root',
    'password': '111Ker0Lar9',
    'host': '127.0.0.1',
    'database': 'library'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

DB_NAME = 'library'

TABLES = {}

TABLES['logs'] = (
    "CREATE TABLE `logs` ("
    " `id` int(11) NOT NULL AUTO_INCREMENT,"
    " `text` varchar(250) NOT NULL,"
    " `user` varchar(250) NOT NULL,"
    " `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)


def login():
    print("please enter your username and password")
    username=input()
    password=input()
    sql = (
        "SELECT * FROM usertable WHERE username=%s AND passwordus=%s")
    cursor.execute(sql, (username,password,))
    result = cursor.fetchall()
    print("   userId  username    password    deptId")
    for i in range(len(result)):
        print(i + 1, " ", result[i][0], "    ", result[i][1], " " * (10 - len(result[i][1])), result[i][2],
              " " * (15 - len(result[i][2])), result[i][3])
login()

def show_userinfo():
    cursor.execute(
        "Select * from usertable")
    result=cursor.fetchall()
    print("   userId  username    password    deptId")
    for i in range(len(result)):
        print(i+1," ",result[i][0],"    ",result[i][1]," "*(10-len(result[i][1])),result[i][2]," "*(15-len(result[i][2])),result[i][3])


def book_reservation():
    print("these books are availabe")
    """print("????????????????????????????????????????")
    sql4=" (SELECT * FROM borrowtable WHERE dateofreturn='NULL')"
    cursor.execute(sql4, ())
    result = cursor.fetchall()
    print(result)
    print("????????????????????????????????????????")"""
    sql2="SELECT * FROM bookinfotable WHERE isbn NOT IN(SELECT isbn FROM booktable WHERE accessino IN (SELECT accessino FROM borrowtable WHERE dateofreturn='NULL'))"
    sql1="SELECT * FROM bookinfotable JOIN booktable USING (isbn) WHERE accessino NOT IN(SELECT accessino FROM borrowtable WHERE dateofreturn=NULL)"
    sql = ("SELECT * FROM bookinfotable WHERE isbn IN(SELECT isbn FROM booktable WHERE accessino  NOT IN(SELECT accessino FROM borrowtable WHERE dateofreturn=NULL))")
    cursor.execute(sql2, ())
    result = cursor.fetchall()
    print("    isbn          author      publisher        title")
    for i in range(len(result)):
        print(i + 1, " ", result[i][0], "    ", result[i][1], " " * (10 - len(result[i][1])), result[i][2],
              " " * (15 - len(result[i][2])), result[i][3])

    print("enter the name the book you want for better search result and if you want to quit the progress write Exit")
    nameBook=input()
    #isbnBook=int(input())
    if(nameBook!="Exit"):
        sql = ("(SELECT * FROM bookinfotable WHERE title= %s)")
        cursor.execute(sql, (nameBook,))
        result1 = cursor.fetchall()
        print("thses books by the name you want  ")
        print("    isbn          author      publisher        title")
        for i in range(len(result1)):
            print(i + 1, " ", result1[i][0], "    ", result1[i][1], " " * (10 - len(result1[i][1])), result1[i][2],
                  " " * (15 - len(result1[i][2])), result1[i][3])
        print("enter the isbn of the book you want and your userid for reserving the book")
        isbn=int(input())
        userid=int(input())
        sql1 = ("(SELECT accessino FROM booktable WHERE isbn=%s)")
        cursor.execute(sql1, (isbn,))
        result2 = cursor.fetchall()
        print("result2",result2)
        today = date.today()
        d1 = today.strftime("%Y/%m/%d")
        sql2="INSERT INTO borrowtable(userid,accessino,dateofborrow,dateofreturn) VALUES(%s,%s,%s,%s)"
        cursor.execute(sql2, (userid,result2[0][0],d1,'NULL',))
        result3=cursor.fetchall()
        db.commit()
        sql3="SELECT COUNT(*) FROM borrowtable"
        cursor.execute(sql3)
        result4=cursor.fetchall()
        print("your borrow id is ",result4[0][0])
        print("you need borrow id for give the book back so keep it")
#book_reservation()
def givebookback():
    today = date.today()
    d1 = today.strftime("%Y/%m/%d")
    print("write the accessino and userid for give the book back")
    #userid=int(input())
    #accessino=int(input())
    borrowid=int(input())
    sql = "UPDATE borrowtable SET dateofreturn = %s WHERE  borrowid=%s"
    cursor.execute(sql,(d1,borrowid,),)
    result=cursor.fetchall()
    print("in give back",result)
    db.commit()
def addbook():
    print("enter the isbn , author , publisher and name of the book you want to add ")
    isbn=int(input())
    author=input()
    publisher=input()
    title=input()
    sql2 = "INSERT INTO bookinfotable(isbn,author,publisher,title) VALUES(%s,%s,%s,%s)"
    cursor.execute(sql2, (isbn,author,publisher,title,))
    result3 = cursor.fetchall()
    db.commit()

    sql3 = "INSERT INTO booktable(isbn) VALUES(%s)"
    cursor.execute(sql3, (isbn,))
    result3 = cursor.fetchall()
    db.commit()
    print("your book is added")


#login()
print("for adding book write AddBook")
print("for reserving book write ReserveBook")
print("for give the book back write GiveBack")
print("for quit the app write Quit")

while(True):
    a=input()
    if a=="AddBook":
        addbook()
    if a=="ReserveBook":
        book_reservation()
    if a=="GiveBack":
        givebookback()
    if a=="Quit":
        exit()

