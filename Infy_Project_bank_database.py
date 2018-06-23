'''
Created on Nov 16, 2017

@author: Abhishek Gupta
'''
import cx_Oracle
conn=cx_Oracle.connect("mayank34/mayank34")
cur=conn.cursor()

cur.execute("create table new_cust(facno varchar2(25),acno number(25) primary key,actype varchar2(10),\
    name varchar2(25),email varchar2(25),aid number(25),contact number(25))")
cur.execute("create table balance(acno number(25) references new_cust(acno) ON DELETE CASCADE,bal number(10,5),sec_depo number(10,5))")
cur.execute("create table trans(acno varchar2(10),dot date,ttype varchar2(10),amt number(8))")
conn.commit()

