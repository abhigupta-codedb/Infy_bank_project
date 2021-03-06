'''
Created on Nov 16, 2017

@author: Abhishek Gupta
'''
import cx_Oracle
import datetime
import time;
from builtins import str
#from curses.ascii import NUL

class cust:
        
    def create_new(self):
        #add new customer
        self.name=input("Enter name--")
        self.actype=input("Enter a/c type(saving/current)--")
        self.email=input("Enter valid email-")
        self.uid=input("Enter Adhaar No.-")
        self.contact=input("Enter Contact No-")
        while(1):
            self.bal=int(input("Enter Opening balance(>500)--"))
             
            if(self.bal<500):
                print("invalid Balance")
             
            elif(self.bal>=500):
                break
        
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select max(acno) from new_cust")
        self.x=cur.fetchone()
        
        if(self.x[0] is None):
            self.x=1000
        else:
            self.x=int(self.x[0])
            self.x=self.x+1
        
        
        if self.actype=="saving":
            self.facno="s"+str(self.x)
        
        if self.actype=="current":
            self.facno="c"+str(self.x)
        
        self.x=str(self.x)
        self.acno=self.x
        conn.close()
        
# return {self.name,self.actype,self.bal,self.acno,self.facno}
        
    def commit1(self):
        self.minval=str(-1)
        self.bal=str(self.bal)
        print("your acc no.",self.facno)
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("insert into new_cust values('"+self.facno+"','"+self.acno+"','"+self.actype+"','"+self.name+"','"+self.email+"','"+self.uid+"','"+self.contact+"')")
        cur.execute("insert into balance values('"+self.acno+"','"+self.bal+"','"+self.minval+"')")
        conn.commit()
        conn.close()    
                
    
    def N_withdrawal(self):
        print("---Welcome to Normal customer Withdrawal---")
        self.acno=input("Enter Acc no.--")
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select acno,sec_depo from new_cust natural join balance where acno='"+self.acno+"'")        
        b=cur.fetchone()
        
        if(b is not None):
            v1=str(b[0])
            v2=str(b[1])
        
            if(v1==self.acno and v2=="-1.0"):
                self.amt=input("Enter Amount--")
                conn=cx_Oracle.connect("mayank34/mayank34")
                cur=conn.cursor()
                cur.execute("select bal from balance where acno='"+self.acno+"'")
                b=cur.fetchone()
                b=int(b[0])
                #print(b)
                ub=b-int(self.amt)
            
                if ub<500:
                    print("Amount exceeds minimum balance limit")
                    self.N_withdrawal()
                else:
                    now = datetime.datetime.now()
                    ub=str(ub)
                    cur.execute("insert into trans values('"+self.acno+"','"+now.strftime("%d-%b-%y")+"','Nor_wthdrw','"+self.amt+"')")
                    cur.execute("update balance set bal='"+ub+"' where acno='"+self.acno+"'")
                    conn.commit()
                    conn.close()
            
            elif(v1==self.acno and v2!="-1.0"):
                print("Withdrawl for Normal customers only! Choose options Wisely!")
                o2.G_withdrawal()
        
            elif(b is None):
                print("Accno. do not exist")
        else:
            print("Invalid Account")
            
    def Deposit(self):
        self.acno=input("enter your accno.--")
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select acno from balance where acno='"+self.acno+"'")
        b=cur.fetchone()
        
        conn.commit()
        conn.close()
        #validating enrty if yes then updating bal table
        
        if(b is not None):
            b=int(b[0])
            
            if(b==int(self.acno)):
                self.amt=input("enter amount--")
                conn=cx_Oracle.connect("mayank34/mayank34")
                cur=conn.cursor()
                cur.execute("select bal from balance where acno='"+self.acno+"'")
                b=cur.fetchone()
                b=int(b[0])
                ub=b+int(self.amt)
                ub=str(ub)
                cur.execute("update balance set bal='"+ub+"' where acno='"+self.acno+"'")
                now = datetime.datetime.now()
                cur.execute("insert into trans values('"+self.acno+"','"+now.strftime("%d-%b-%y")+"','Deposit','"+ub+"')")
                conn.commit()
                conn.close()
            
            else:
                print("Account Not found") 
        else:
            print("Invalid Account")
                
    def Search(self):
        self.facno=input("enter account no.--")
        #self.facno=str(self.facno)
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select facno from new_cust where facno='"+self.facno+"'")
        b=cur.fetchone()
        
        if(b is not None):
            #b=int(b[0])
            #print(b)
            if(b[0]==self.facno):
                cur.execute("select * from new_cust natural join balance where facno='"+self.facno+"'")
                b=cur.fetchone()
                #print(b)
                print("-------------------")
                print("Accoun Holder-",b[3])
                print("Account No.-",b[1])
                print("Account Type-",b[2])
                print("Account Balnc-",b[7])
                if(int(b[5])==-1):
                    print("Customer Type-Normal")
                else:
                    print("Customer Type-Gold")
                print("-------------------")        
                conn.close()
            else:
                print("Record not found!")
        else:
            print("Invalid Account")
              
    def delete(self):
        self.acno=input("Enter account no.--")
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select acno from new_cust where acno='"+self.acno+"'")
        b=cur.fetchone()
        conn.close()
        if(b is not None and int(b[0])==int(self.acno)):
            conn=cx_Oracle.connect("mayank34/mayank34")
            cur=conn.cursor()
            #print(self.acno,"self.acno")
            cur.execute("delete from new_cust where acno='"+self.acno+"'")
            conn.commit()
            print("Record deleted")
            conn.close()
        elif(b is None):
            print("Record not found")
            
                     
class gold_cust(cust):
    
    def create_new(self):
        super(gold_cust,self).create_new()
        self.sec_depo=input("Enter security deposit--")
            
            
        
    def commit2(self):
        self.bal=str(self.bal)
        print("your acc no.",self.facno)
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("insert into new_cust values('"+self.facno+"','"+self.acno+"','"+self.actype+"','"+self.name+"',\
        '"+self.email+"','"+self.uid+"','"+self.contact+"')")
        cur.execute("insert into balance values('"+self.acno+"','"+self.bal+"','"+self.sec_depo+"')")
        conn.commit()
        conn.close()    
        
    def G_withdrawal(self):
        print("---Welcome to Gold customer Withdrawal---")
        self.acno=input("Enter Acc no.--")
        conn=cx_Oracle.connect("mayank34/mayank34")
        cur=conn.cursor()
        cur.execute("select acno,sec_depo from new_cust natural join balance where acno='"+self.acno+"'")        
        b=cur.fetchone()
        
        if(b is not None):
            v1=str(b[0])
            v2=str(b[1])
        
            if(v1==self.acno and v2!="-1.0"):
                self.amt=input("Enter amount--")
                conn=cx_Oracle.connect("mayank34/mayank34")
                cur=conn.cursor()
                cur.execute("select bal from balance where acno='"+self.acno+"'")
                b=cur.fetchone()
                b=int(b[0])
                #print(b)
                ub=b-int(self.amt)
            
                if ub<300:
                    print("Amount exceeds minimum Gold balance limit try again!")
                    self.G_withdrawal()
                else:
                    now = datetime.datetime.now()
                    ub=str(ub)
                    cur.execute("insert into trans values('"+self.acno+"','"+now.strftime("%d-%b-%y")+"','gld_wthdrw','"+self.amt+"')")
                    cur.execute("update balance set bal='"+ub+"' where acno='"+self.acno+"'")
                    conn.commit()
                    conn.close()
            
            elif(v1==self.acno and v2=="-1.0"):
                print("Withdrawl for Gold customers only! Choose options Wisely!")
                self.N_withdrawal()
        
            elif(b is None):
                print("Accno. do not exist")
         
        else:
            print("Invalid Account Number!")
        
ans='y'
while ans=='y':
    print("----------------------------")
    print(" Create Customer (Normal)--1")
    print(" *****Withdrawal (Normal)--2")
    print(" **Create Customer (Gold)--3")
    print(" *******Withdrawal (Gold)--4")
    print(" ***********Deposit (N/G)--5")
    print(" ************Search (N/G)--6")
    print(" ************Delete (N/G)--7")
    print("----------------------------")
    
    o1=cust()
    o2=gold_cust()
    
    ch=int(input("Enter your choice--"))
    if ch==1:
        o1.create_new()
        o1.commit1()
    elif ch==2:
        o1.N_withdrawal()
    elif ch==3:
        o2.create_new()
        o2.commit2()
    elif ch==4:
        o2.G_withdrawal()        
    elif ch==5:
        o1.Deposit()
    elif ch==6:
        o1.Search()
    elif ch==7:
        o1.delete()            
    else:
        print("Invalid choice")
    
    ans=input("To Continue...y/n--")
