import PySimpleGUI as sg
from datetime import date
import helper_functions
import mysql.connector

server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd)
cur = conn.cursor()

def mainform():
    DataValues=[]
    total=0
    
    Keylist=['ORDER','DATE','ITEMID','ITEM NAME','ORIGIN','UNIT PRICE','QUANTITY','AMOUNT','AVAILABLE','TOTAL']
    Headings=['Order','Date','Item ID','Item name','Origin','Unit price','Quantity','Amount']
    Headings1=['Order','Item ID','Item name','Origin','Unit price','Quantity','Amount']
   
    
    Panel=[[sg.Text(Headings[0],size=11),sg.Input(size=20,key=Keylist[0]),
        sg.Text(Headings[1],size=11),sg.Input(size=20,key=Keylist[1],readonly=True),
        sg.Text(Headings[2],size=11),sg.Input(size=20,key=Keylist[2])],   
        
        [sg.Text(Headings[3],size=11),sg.Input(size=20,key=Keylist[3]),sg.Text(Headings[4],size=11),sg.Input(size=20,key=Keylist[4]),sg.Text('Available',size=11),sg.Input(size=20,key=Keylist[8],readonly=True)], 
        [sg.Text(Headings[5],size=11),sg.Input(size=20,key=Keylist[5]),
        sg.Text(Headings[6],size=11),sg.Input(size=20,key=Keylist[6],tooltip='Less than or equal available quantity'),sg.Text(Headings[7],size=11),sg.Input(size=20,key=Keylist[7],readonly=True)],
        [sg.Button('Add row',size=10),sg.Button('Find',size=10),sg.Button('PDF',size=10,disabled=True),sg.Button('Delete row',size=10),sg.Button('Update',size=10,focus=True),sg.Button('Reset',size=10),sg.Button('QR scan',size=10),sg.Button('Exit',size=10)],
        [sg.Text('Total sum: ',size=8),sg.Text('Amount',size=8,key='Total')]]

    layout=[[sg.Frame('Item details',Panel)],
        [sg.Table(DataValues,Headings1,justification='left',key='mytable',enable_events=True,size=(200,10),expand_x = True)]]
    window=sg.Window('Product Management',layout)
    
    while True:
        event,values=window.read() 
        if event in (None, 'Exit'):
          break       
      
        if event=='Reset':
            helper_functions.Reset_data_selling(window,Keylist)
            
        if event=='QR scan':
            item_id=helper_functions.QR_trace()
            print(item_id)
            sql1="select * from quotation where product_id='"+item_id+"'"
            data1=helper_functions.table_read(conn,sql1,1,3)
            
            #Take the lastest price_id 
            if data1==[]:
                sg.popup('Item dont have price_id')
                continue
            price_id=data1[len(data1)-1][0]
            sql="select quotation.product_id as id,product_name,origin,price,available_quantity from quotation,product "
            sql+="where quotation.product_id=product.product_id and price_id='"+price_id+"'" #Finding item in4 by item_id
          
            Data=helper_functions.table_read(conn,sql,0,5)   #DataValues=table_read(conn,sql)
            Data_row=Data[0]
            
            #Insert some details to display on grid
            Data_row.insert(0,len(DataValues)+1)        #Insert num column
            Data_row.insert(5,1)                        #Insert quantity column
            Data_row.insert(6,int(Data_row[4]))         #Insert amount column
            today=date.today()
            
            if DataValues==[]:
                DataValues.append(Data_row)
            else:
                for row in DataValues:
                    if row[1]==item_id:
                        print('This item is already in the order')
                        break
                    else:
                        DataValues.append(Data_row)
                        break
                    
            for row in DataValues:
                total+=int(row[6])
                
            window['Total'].update(str(total))
            window['mytable'].update(values=DataValues)
            
            today=date.today()
            window[Keylist[1]].update(value=today)
            sql="select * from selling where date='"+str(today)+"' order by ordinal_num ASC" #Generating order ID
            
            OR_List=helper_functions.table_read(conn,sql,0,2)
            if OR_List==[]:
                Order_id="OD"+str(today)+"-0001"
            else:
                Last_or=OR_List[len(OR_List)-1]
                ID=Last_or[1]
                ID_list=ID.split("-")
                num=int(ID_list[3])+1
                if num<10:
                    Order_id='OD'+str(today)+'-000'+str(num)
                if num>=10 and num<100:
                    Order_id='OD'+str(today)+'-00'+str(num)
                if num>=100 and num<1000:
                    Order_id='OD'+str(today)+'-0'+str(num)
                if num>=100 and num<10000:
                    Order_id='OD'+str(today)+'-'+str(num)
                    
            for i in range(2,9):
                window[Keylist[i]].update(value=Data_row[i-1])
            window['PDF'].update(disabled=False)
            
        if event=='Find':
            
            price_id=None
            if values['ITEMID']!='':
                item_id=values['ITEMID']
                sql1="select * from quotation where product_id='"+item_id+"'"
                data1=helper_functions.table_read(conn,sql1,1,3)
                
                if data1!=[]:
                    price_id=data1[len(data1)-1][0]  #Take the lastest price_id
               
            if price_id==None:
                sg.popup('Item dont have price_id')     
                continue
            sql="select quotation.product_id as id,product_name,origin,price,available_quantity from quotation,product "
            sql+="where quotation.product_id=product.product_id and price_id='"+price_id+"'" #Finding item in4 by item_id
          
            Data=helper_functions.table_read(conn,sql,0,5)   #DataValues=table_read(conn,sql)
            Data_row=Data[0]
            
            #Insert some details to display on grid
            Data_row.insert(0,len(DataValues)+1)        #Insert num column
            Data_row.insert(5,1)                        #Insert quantity column
            Data_row.insert(6,int(Data_row[4]))         #Insert amount column
            
            today=date.today()
            window[Keylist[1]].update(value=today)
            
            sql="select * from selling where date='"+str(today)+"' order by ordinal_num ASC" #Generating order ID
            OR_List=helper_functions.table_read(conn,sql,0,2)
            
            if OR_List==[]:
                Order_id="OD"+str(today)+"-0001"
            else:
                Last_or=OR_List[len(OR_List)-1]
                ID=Last_or[1]
                ID_list=ID.split("-")
                num=int(ID_list[3])+1
                
                if num<10:
                    Order_id='OD'+str(today)+'-000'+str(num)
                if num>=10 and num<100:
                    Order_id='OD'+str(today)+'-00'+str(num)
                if num>=100 and num<1000:
                    Order_id='OD'+str(today)+'-0'+str(num)
                if num>=100 and num<10000:
                    Order_id='OD'+str(today)+'-'+str(num)
                    
            for i in range(2,9):
                window[Keylist[i]].update(value=Data_row[i-1])
            window['PDF'].update(disabled=False)
            
        if event=='mytable':
            if values['mytable']==[]:
                sg.popup('No row selected')
                
            else:
                editRow=values['mytable'][0]            
                Erow=DataValues[editRow]   
                today=date.today()
                d=today.strftime("%d/%m/%Y")
                
                window[Keylist[1]].update(value=d)  
                   
                for i in range(1,8):
                    window[Keylist[i+1]].update(value=Erow[i]) 
                    
                window[Keylist[0]].update(value=Order_id)
                window['PDF'].update(disabled=False)
                
        if event=='Update':
            flag=True
            
            for i in range(1,8):
                if values[Keylist[i]]=='':
                    flag=False
                    break
                
            if int(values['QUANTITY'])>int(values['AVAILABLE']):
                flag=False
                sg.popup('Quantity must be less than or equal available_num')
            else:
                flag=True
                
            if flag==True:
                try:
                    quantity=int(values['QUANTITY'])
                    unit_price=int(values['UNIT PRICE'])
                    total_price=quantity*unit_price
                    window['AMOUNT'].update(str(total_price))
                    values[Keylist[7]]=total_price
                except:
                    sg.popup('Quantity and unit_price must not be negative')
                    
                product_ID=values[Keylist[2]]
                
                for i in range(len(DataValues)):
                    if DataValues[i][1]==product_ID:
                        
                        for j in range(2,8):
                            DataValues[i][j-1]=values[Keylist[j]]      
                                                
                # Update the displayed table
                window['mytable'].update(values=DataValues)
                total=0
                #Loop to clean box
                for row in DataValues:
                    total+=int(row[6])
                    
                window['Total'].update(str(total))
                window[Keylist[0]].update(value=Order_id)
                
        if event=='Add row':
            flag=True
            for i in range(0,8):
                if values[Keylist[i]]=='':
                    flag=False
                    break
                
            if int(values['QUANTITY'])>int(values['AVAILABLE']):
                flag=False
                sg.popup('Quantity must be less than or equal available_num')
            else:
                flag=True
            ms=values['ITEMID']
            
            for row in DataValues: #Dont accept item already in list
                    if row[1]==ms:
                        sg.popup('This item is already in the order')
                        flag=False
                        break
                    
            if flag==True:
                
                try:
                    quantity=int(values['QUANTITY'])
                    unit_price=int(values['UNIT PRICE'])
                    total_price=quantity*unit_price
                    
                    window['AMOUNT'].update(str(total_price))
                    values[Keylist[7]]=total_price
                except:
                    sg.popup('Quantity and unit_price must not be negative')
                    
                for i in range(2,9):
                    Data_row[i-1]=values[Keylist[i]]
                DataValues.append(Data_row)   
                                   
                # Update the displayed table
                window['mytable'].update(values=DataValues)
                total=0
                #Loop to clean box
                for row in DataValues:
                    total+=int(row[6])
                    
                window['Total'].update(str(total))
                helper_functions.Reset_data_selling(window,Keylist)
                
        if event =='Delete row':
            
            if values['mytable']==[]:
                sg.popup('No row selected')
                
            else:
                if sg.popup_ok_cancel('Can not undo Delete : Contine?')=='OK':
                    
                    # Update the DataBase
                    editRow=values['mytable'][0] 
                    del DataValues[values['mytable'][0]]      
                                                         
                    # Update the displayed table
                    window['mytable'].update(values=DataValues)
                    helper_functions.Reset_data_selling(window,Keylist)
                    total=0
                    
                    for row in DataValues:
                        total+=int(row[6])
                window['Total'].update(str(total))
                
        if event=='PDF':
            today=date.today()
            
            if DataValues!=[]:
                for row in DataValues:
                    OI=Order_id
                    OD=date.today()
                   
                    sub=int(row[7])-int(row[5])
                    sql="INSERT INTO selling (ordinal_num,order_id,date,Item_id,Volumn,Unit_price,Amount) VALUES (Null,'"+str(OI)+"','"+str(OD)+"','"+str(row[1])+"','"+str(row[5])+"','"+str(row[4])+"','"+str(row[6])+"')"
                    cur.execute(sql)
                    sql="UPDATE product SET available_quantity='"+str(sub)+"'WHERE product_id='"+row[1]+"';"
                    cur.execute(sql)
                    
                helper_functions.PDF_extract_selling(DataValues,Order_id,str(today),str(total))
                helper_functions.Reset_data_selling(window,Keylist)
                DataValues=[]
                window['mytable'].update(values=DataValues)
                
            else:
                sg.popup('Dữ liệu nhập thiếu')                 
    # if conn:
    #     conn.close()
    window.close() 
