import urllib.request
from urllib.error import HTTPError
import re
from tkinter import *
#from tkinter.ttk import *
import pandas as pd
import time



root = Tk()
root.geometry('500x500')
root.configure(bg='#fffae6')
root.title('Stock data')

#mapping
companies = {"apple" : "AAPL",
         "google" : "GOOG",
         "microsoft" : "MSFT",
         "tata motors" : "TATAMOTORS",
         "adani power limited" : "ADANIPOWER",
         "reliance" : "RELIANCE",
         "tcs" : "TCS",
         "hdfc" : "HDB",
         "icici" : "ICICIBANK",
            "wipro":"WIPRO"}

def myEntry():
    com = e.get()
    df = e1.get()
    mf = e2.get()
    yf = e3.get()
    dt = e4.get()
    mt = e5.get()
    yt = e6.get()
    com = companies[com]
    e.delete(0,'end')
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')
    e5.delete(0,'end')
    e6.delete(0,'end')
    stock(com,df,mf,yf,dt,mt,yt)
    

def stock(com,df,mf,yf,dt,mt,yt):
    p1 = '\d{4}[-]\d{2}[-]\d{2}'
    p2 = '[A-Z]{3,15}'
    #p3 = '\d{1,6}[.]?\d{1,4}'

    date = []; symbol = []; op = []; high = []; low = []; close = []; vol = []; af_hrs = []; pre_market = []

    m1 = int(mf); m2 = int(mt); d1 = int(df); d2 = int(dt); y1 = int(yf); y2 = int(yt)
    
    for i in range(y1,y2+1):
        
        if(i==y1==y2):
            month = m1
            m = m2
        elif(i==y2 and i!=y1):
            m = m2
            month = 1
        elif(i==y1 and i!=y2):
            m = 12
            month = m1
        else:
            m = 12
            month = 1
        #print(month,m)

        for j in range(month,m+1):
            
            th = [4,6,9,11];th1 = [1,3,5,7,8,10,12]
            
            if (i==y1 and i!=y2):
                if(j==m1):
                    day = d1
                else:
                    day = 1
                if(j in th):d = 30
                elif(j in th1):d = 31
                elif(j==2 and i%4==0):d = 29
                elif(j==2 and 1%4!=0):d = 28

                
        
            elif (i==y2 and i!=y1):
                if(j==m2):
                    day = 1;d = d2
                
                else:
                    day = 1
                    if(j in th):d = 30
                    elif(j in th1):d = 31
                    elif(j==2 and i%4==0):d = 29
                    elif(j==2 and 1%4!=0):d = 28
                        
            elif (i==y1 and i==y2):
                if(j==m1 and j==m2):
                    day = d1
                    d = d2
                elif(j==m1 and j!=m2):
                    day = d1
                    if(j in th):d = 30
                    elif(j in th1):d = 31
                    elif(j==2 and i%4==0):d = 29
                    elif(j==2 and 1%4!=0):d = 28
                elif(j==m2 and j!=m1):
                    day = 1
                    d = d2
                    
                    
            elif (i!=y1 and i!=y2):
                day = 1
                if(j in th):d = 30
                elif(j in th1):d = 31
                elif(j==2 and i%4==0):d = 29
                elif(j==2 and 1%4!=0):d = 28
            #print(day,d)


            for k in range(day,d+1):
                time.sleep(20)
                yf = str(i); mf = str(j); df = str(k)
                
                if(len(mf)==1 and len(df)==1):
                    mf='0'+mf
                    df='0'+df
                elif(len(df)==1 and len(mf)!=1):
                    df='0'+df
                elif(len(mf)==1 and len(df)!=1):
                    mf='0'+mf
                print(com,yf,mf,df)
                try:
                    url = 'https://api.polygon.io/v1/open-close/'+com+'/'+yf+'-'+mf+'-'+df+'?adjusted=true&apiKey=YI6GkVN0nLj66T_UlHkKNLU9sBZ6AzdN'
                    response = urllib.request.urlopen(url)
                    content = response.read()
                    response.close()
                except HTTPError as err:
                    if err.code == 404:
                        continue
                    else:
                        raise 
                con = content.decode()
                conn = eval(con)
                print(conn)
                x1 = re.findall(p1,con)
                x2 = re.findall(p2,con)
                #x3 = re.findall(p3,con)
                print(x1,x2)
                date.append(x1[0])
                symbol.append(x2[0])
                op.append(conn['open'])
                high.append(conn['high'])
                low.append(conn['low'])
                close.append(conn['close'])
                af_hrs.append(conn['afterHours'])
                pre_market.append(conn['preMarket'])
                vol.append(str(conn['volume']))
                print(date,op,close)
    file(date,symbol,op,high,low,close,vol,af_hrs,pre_market)

def file(date,symbol,op,high,low,close,vol,af_hrs,pre_market):
    data = pd.DataFrame({'Date':date,'Symbol':symbol,'Open':op,'High':high,'Low':low,'Close':close,
                         'Volume':vol,'After_hours':af_hrs,'Pre_market':pre_market})
    data.to_csv(r"C:\Users\Sushma Sharma\Downloads\stock_data.csv",index=False)


label = Label(root,text = 'Enter the dates for stock price data',font=("Arial", 15)).place(x=110,y=30)

label1 = Label(root,text = 'Company name').place(x=160,y=110)
e = Entry(root,width=20)
e.place(x=270,y=110)

l1 = Label(root,text = 'From',font=("Arial", 10)).place(x=130,y=170)

l3 = Label(root,text = 'Day').place(x=190,y=145)
l4 = Label(root,text = 'Month').place(x=260,y=145)
l5 = Label(root,text = 'Year').place(x=350,y=145)

e1 = Entry(root,width = 10)
e1.place(x = 170,y = 170)
e2 = Entry(root,width = 10)
e2.place(x = 250,y = 170)
e3 = Entry(root,width = 10)
e3.place(x = 330,y = 170)

l2 = Label(root,text = 'To',font=("Arial", 10)).place(x=130,y=210)

e4 = Entry(root,width = 10)
e4.place(x = 170,y = 210)
e5 = Entry(root,width = 10)
e5.place(x = 250,y = 210)
e6 = Entry(root,width = 10)
e6.place(x = 330,y = 210)

button = Button(root,text='Submit',fg='white',bg='pink',font=('Broadway',12),command=myEntry).place(x=240,y=250)
button1 = Button(root,text='Exit',fg='white',bg='gray',font=('Broadway',12),command=root.destroy).place(x=255,y=290)
root.mainloop()
