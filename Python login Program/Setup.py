#import mysql.connector as sql
import pandas as pd
import numpy as np
import mysql.connector as sql

Storehouse=sql.connect(host='localhost',user='root',passwd='jayant1234')
mycursor=Storehouse.cursor()

#SQL SERVER CONNECTION       
def CreateTB(Store):
        try:
                mycursor.execute('use PassHome;')
                try:
                        mycursor.execute('CREATE TABLE %s(Name varchar(20),Username varchar(20),Password varchar(20));'\
                                 %(Store))
                except:
                       # print("live storing..")
                        pass
                Storehouse.commit()
        except:
                Storehouse.rollback()
                mycursor.execute("CREATE DATABASE %s;"%('PassHome'))
                mycursor.execute('use PassHome')
                mycursor.execute('CREATE TABLE %s(Name varchar(20),Username varchar(20),Password varchar(20));'\
                                     %(Store))
                Storehouse.commit()

#USER INFORMATION UPLOADING IN SQL DATABASE
def RecDB(name,user,passwd):
        mycursor.execute("insert into Vitals values('%s','%s','%s')"%(name,user,passwd))
        Storehouse.commit()

#========================================DATA MANUPULATION FUNCTIONS==================
#CUSTOMER_USERNAME_INPUT
def username(floor):
    while True:
        ask=input('Enter username:')
        check=len(ask)
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*~'''
        for pun in punctuations:
            if pun in ask:
                print("Punctuations are not allowed.Please enter characters only")
                continue
            
        if check<floor:
            print("The Username should not be less than %i characters"%floor)
            continue
        
        elif check >= floor:
            return ask
            break


#CUSTOMER_PASSWORD_INPUT    
def password(limit):
    while True:
        ask=input('Enter password')
        check=len(ask)
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*~'''
        for pun in punctuations:
            if pun in ask:
                print("Punctuations are not allowed.Please enter characters only")
                continue 
        if check<limit:
            print("The Passwords should not be less than %i characters"%limit)
            continue
        elif check >= limit:
            return ask
            break

        


            
#NUMERIC-ALPHABET INPUT LIMITATION           
def limitalnum(content):
        punctuations =['!','(',')','-','[',']','{','}',';',':',"'",'"',"\\",',','<','>','.','/','?','@','#','$','%','^','&','*','_','~']
        count=3
        while True:
            ask_input=input("%s"%content)
            if ask_input.isalnum()==False:
                count=count-1
                if count in[3,2,1]:
                    print("Sorry only alphabets and numeric are acceptable")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
                continue
            else:
                return ask_input 
                break

            
#NUMERICALS INPUT LIMITATION 
def num(content):
        count=3
        while True:
            try:
                var=int(input('%s'%content))
                return var
                break
            except ValueError:
                count=count-1
                if count in[3,2,1]:
                    print("Invalid Data type found")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break


#CHARACTER INPUT LIMITATION 
def Convchar(content):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*~'''
        values=''
        count=3
        while True:
            variable_space=input("%s"%content)
            if variable_space!=0:
                for val in variable_space:
                    if val not in punctuations:
                        values=values+val
                return values
                break
            else:
                count=count-1
                if count in[3,2,1]:
                    print("Invalid Data type found")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
                continue

#=============================================================================================

#DATA RECONCILATION

data_package=123456789
def check(first,sec):
    global data_package
    data_package=1
    while True:   
        if first == sec:
            print('Password sucessfully matched')
            Storehouse.commit()
            break
        elif first != sec:
            Storehouse.rollback()
            print("Password failed to match")
            Registar()
            break
            

#LOGIN VERFICATION       
def Console(First,Second):
    while True:
        if First not in  Second:
            print("Fields did not match succesfully")
            break 
        elif First==Second:
            print('Continuing')
            USERLOG()


#INPUT CLEANSING 
def pop(word):
    alphabets=['a','q','e','w','r','t','y','u','i','o','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0']
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in word:
       if char in alphabets:
           no_punct = no_punct + char
    return no_punct



#SPACE CLEANER 
def Replace_spc(string):
    return string.replace(' ', '')



#REGISTRATION OF CUSTOMER WITH LOGIN DETAILS 
def Registar():
        
        a=Convchar('Enter Name')
        Cust_user=username(2)
        Cust_passwd=password(8)
        d=Convchar("Enter Confirmed password:")
        check(Cust_passwd,d)
        if data_package == 1:
                RecDB(a,Cust_user,Cust_passwd)
                Storehouse.commit()
        elif data_package == 0:
                pass
        else:
                pass
        return Cust_user
        return Cust_passwd
        Storehouse.close()

#USER DATA TAKING FROM SQL DATABASE FOR VERIFICATION
name=[]
user=[]
passwd=[]
log_user=np.array([])
log_passwd=np.array([])
def SearchRTB():
        try:
                global log_user
                global log_passwd
                mycursor.execute("use passhome;")
                mycursor.execute("select * from vitals;")
                record=mycursor.fetchall()
                for row in record:
                    name.append(row[0])
                    user.append(row[1])
                    passwd.append(row[2])
                Table_Data={'Name':name,'Username':user,'Password':passwd}
                Table=pd.DataFrame(Table_Data)
                #return Table
                #print(user)
                log_user=np.array(user)
                log_passwd=np.array(passwd)
                Storehouse.commit()
        except:
                print("No records been found")
                Storehouse.rollback()



#AUTO-DATA CONNECTION IN BACKGROUND
#CreateTB('Vitals')
#SearchRTB()


def SRC_USER(child):
        global log_user
        #print('Matching with:',log_user)
        if child in log_user:
                #print("WIth this:",child)
                #print('USERNAME MATCHED')
                pass
        elif child not in log_user:
                print("The username is invalid.Please enter again")
                USERLOG()
       

        

def SRC_PASSWD(child):
        #print('PASS matching this:',child)
        global log_passwd
        if child in log_user:
                #print('PASSWORD MATCHED')
                pass
        elif child not in log_passwd:
                print('The password is invalid.Please enter again')
                PASSLOG()
        
def USERLOG():
        print("""==================================================================\n                           USER LOGIN PAGE\n\
==================================================================""")
        print('')
        l_user=username(1)
        SRC_USER(l_user)

def PASSLOG():
        p_passwd=password(1)
        SRC_PASSWD(p_passwd)
        
def USERFACE():
        USERLOG()
        PASSLOG()
        Storehouse.close()








    


