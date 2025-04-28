import mysql.connector as mysql_connector
import sys
from time import time
from colorama import init
from termcolor import colored
from random import choice
from db import DB

class Connector:
    def __init__(self):

        self.db = DB()
        self.host = None
        self.port = None
        self.user = None
        self.passwd = None

    def run(self):
        self.input_data()
        self.connect()
        self.use_mysql()

    def show_saved_data(self):
        n = 0
        for host in self.db:
            n += 1
            print(f"{n} => {host}  : {self.db[host]['user']}")


        num = input("~> Enter Host number : ")
        try:
            num  = int(num)
        except:
            print("Invalid Number, Please select from the given number")
            num = 0
        
        st =  self.set_from_saved_data(num = num)
        if not st:
            print("Please select valid options..")
            self.close()

        return True



    def set_from_saved_data(self, num: int) -> bool:
        n = 0
        for host in self.db:
            n += 1

            if n == num:
                self.host = host
                self.user = self.db[host]['user']
                self.passwd = self.db[host]['passwd']
                self.port = self.db[host]['port']

                return True
            
        return False

            
    def destruct_host(self, host: str):
        if len(host.strip())== 0:
            self.host = 'localhost'
            self.port = 3306 
            return 

        
        host_data = host.split(":")
        self.host = host_data[0]

        try:
            self.port = int(host_data[1].strip())
        except:
            if ":" in host:
                print("Input is invalid.. Please read the documentation..")
                exit()

            self.port = 3306 

    
    def close(self):
        print("Press ENTER to quit.. ", end="")
        input("")
        exit()

    def input_data(self):
        host = input("~> Enter HOST : ")
        
        if host == "use":
            self.show_saved_data()
            return

        elif host == "--hack":
            pass

        else:
            self.destruct_host(host)

        self.user = input("~> Enter username : ")
        if len(self.user.strip()) == 0:
            print("Please enter something...")
            self.close()

        self.passwd = input("~> Enter passwd : ")
        if len(self.passwd.strip()) == 0:
            print("Please enter Password...")
            self.close()    

        
    def connect(self):
        try:
            self.conn = mysql_connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                port = self.port
            )

            self.cursor = self.conn.cursor()
    

            self.db[self.host] = {
                    "user" : self.user,
                    "passwd" : self.passwd,
                    "port" : self.port
                }
            print(f"Info is saved.. for future use...")

        except Exception as e:
            print(e)
            print("Error in connecting to the MySql Server..")
            self.close()



    def use_mysql(self):
        input_text = 'MySql'#
        use_db = ""
        
        while True:
            # print('\n')
            
            print(colored(input_text + use_db + '> ', 'blue'), end='')    

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
                    self.cursor.execute(c)
                    if c.split(' ')[0] in ['create','alter','insert','drop','update','delete','use']:
                        self.conn.commit()

                    if c.split(' ')[0]=='use':
                        print(colored('Database changed', 'yellow'))
                        use_db = c.replace("use", "").replace(";", "").strip()
                        use_db = f" ({use_db})"
                        use_db = colored(use_db, 'green')
                        
                    
                    else:
                        
                        count=0
                        
                        data=[]
                        count_lst=[]
                        i=0

                        for col in self.cursor.column_names:
                            try:
                                if   len(str(col)) > count_lst[i]:
                                                            
                                    count_lst.pop(i)
                                    count_lst.insert(i,len(str(col)))
                                
                            except:
                                count_lst.append(len(str(col)))
                            i+=1
                            
                        for row in self.cursor.fetchall():
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
                            for col in self.cursor.column_names:
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
                            
                            p=' '+str(self.cursor.rowcount)+' rows in set ('+str(time()-tb)[:4]+' Sec)'
                            print(colored(p, 'cyan'))
                            
                        else:
                            print(colored('Query OK,', 'yellow'),end='')
                            p=' '+str(self.cursor.rowcount)+' row affected ('+str(time()-tb)[:4]+' Sec)'
                            print(colored(p, 'cyan'))

                            
                except Exception as e:
                    e='ERROR : '+str(e)+'\n'
                    print(colored(e, 'red'))
                    


        self.conn.close()




        

if __name__ == "__main__":
    conn = Connector()
    conn.run()