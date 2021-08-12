import mysql.connector as sqlcon

conn=sqlcon.connect(host='localhost',user='root',passwd='root',db='root')

if conn.is_connected() == False:
    print('Error in connection')
    
else:
    cursor=conn.cursor()
    cursor.execute("delete from records where name='Sis'")
    conn.commit()
    
    cursor.execute('Select * from records')
    for row in cursor.fetchall():
        print(row,'\n')
    conn.close()
    
