import Setup as ST
#import mysql.connector as sql
import pandas as pd 



def Interface():
        print("""==================================================================\n                           USER LOGIN PAGE\n\
==================================================================""")
        print('')
        print('     1.Login                       2.Register')
        print('')
        print("""==================================================================""")

        user_ask=ST.num('Enter your mode(1/2):')
        if user_ask == 1:
                ST.USERFACE()
                print("""==================================================================""")
                print('')
                QL.Main()       
        elif user_ask==2:
                ST.Registar()
                Restart()
     
def Jump():
        ST.CreateTB('Vitals')
        ST.SearchRTB()
        Interface()

def Restart():
    print("(Enter any keyword to exit)")
    Run_again=input('Press Enter to go to the Menu:')
    if Run_again.lower() == '':
            ST.SearchRTB()
            Jump()
    elif Run_again!='':
        exit()

def Main():
        Jump()

Main()
