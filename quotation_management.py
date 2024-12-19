import PySimpleGUI as sg

import mysql.connector
import helper_functions

server = '127.0.0.1'
db = 'minimart'
username = 'root'
pwd = ''
conn = mysql.connector.connect(host=server, database=db, user=username, password=pwd,use_unicode=True, charset="utf8")
cur = conn.cursor()

# File_types for image
file_types = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]

def quotation():
    sql = 'select * from quotation ORDER BY ordinal_num ASC'
    DataValues=helper_functions.table_read(conn,sql,1,6)
    D_Datavalues=DataValues

    Keylist=['price_id','product_id','price','date', 'supplier']
    Headings=['Price_ID','Product_ID','Price','Applied_Date', 'Supplier']

    Panel=[[sg.Input(size=10,key=Keylist[0],visible=False),
        sg.Text(Headings[1],size=11),sg.Input(size=13,key=Keylist[1],focus=True),sg.Button('Add row',size=(9,1)),sg.Exit(size=(9,1))],
            [sg.Text(Headings[2],size=11),sg.Input(size=13,key=Keylist[2]),sg.Button('Delete row',size=(9,1)),sg.Button("Reset",size=(9,1))],
        [sg.Text(Headings[3],size=11),sg.Input(size=13,key=Keylist[3],readonly=True),sg.CalendarButton('Pick date', close_when_date_chosen=True,  target=Keylist[3], location=(0,0), no_titlebar=False, size=9),sg.Button('Save Edit',disabled=True,size=(9,1))],
        [sg.Text(Headings[4],size=11),sg.Input(size=(13,1),key=Keylist[4]),sg.Button('QR scan',size=(9,1)),sg.Button('PDF FILE',size=(9,1),disabled=True)]
    ]

    layout=[[sg.Frame('INFORMATION ABOUT THE QUOTATION',Panel,expand_x = True)],
        [sg.Table(D_Datavalues,Headings,justification='left',key='mytable',enable_events=True,size=(200,10))]]
    window=sg.Window('Quotation Management',layout)

    while True:
        event,values=window.read() 
        if event in (None, 'Exit'):
          break      
               
        if event=='Reset':
            helper_functions.Reset_data_quotation(window,Keylist) 

        flag=True
        if event=='Add row':
            values[Keylist[0]]=helper_functions.create_price_id(DataValues) 
                             
            # Check if all fields are filled
            for i in range(5):
                if values[Keylist[i]]=='':
                    flag=False
                    
            if flag==True:                      

                old_date=values[Keylist[3]][:10]
                new_date=helper_functions.Format_Date(old_date)
                
                # Update the displayed table       
                D_Datavalues.append([values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],new_date,values[Keylist[4]]])
                DataValues.append([values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],new_date,values[Keylist[4]]])
                
                # Reset the input boxes
                helper_functions.Reset_data_quotation(window,Keylist)
            
                #Cập nhật vào DataBase
                rw=[values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],values[Keylist[3]],values[Keylist[4]]]
            #             price_id          product_id           price             date               supplier  
            
                sql="INSERT INTO quotation (ordinal_num,price_id,product_id,price,Applied_date, supplier) VALUES (Null,'"
                sql+=str(rw[0])+"','"+str(rw[1])+"','"+str(rw[2])+"','"+str(rw[3])+"','"+str(rw[4])+"');"     
                cur.execute(sql)   
                window['mytable'].update(values=D_Datavalues)         
            else:
                sg.popup('Not enough data')

        if event =='mytable':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:            
                # Find the row selected on the Table
                editRow=values['mytable'][0]                 
                Erow=D_Datavalues[editRow]     
                      
                td_update=[Erow[0],Erow[1],Erow[2],Erow[3],Erow[4]]
                # Update the Form Update
                for i in range(5):
                    window[Keylist[i]].update(value=td_update[i])            
                window['Save Edit'].update(disabled=False)
                window['PDF FILE'].update(disabled=False) 
            
        if event=='Save Edit':
            # Check if all fields are filled
            flag=True
            for i in range(4):
                if values[Keylist[i]]=='':
                    flag=False
                    break
                
            if flag==True:            
                product_ID=Erow[0]                      
                td=[values[Keylist[0]],values[Keylist[1]],values[Keylist[2]],values[Keylist[3]],values[Keylist[4]]]
                
                # Update the edited value for D_Datavalues
                for i in range(len(D_Datavalues)):
                    if D_Datavalues[i][0]==product_ID:
                        D_Datavalues[i]=td                                       
                # Update the edited value for DataValues
                for i in range(len(DataValues)):
                    if DataValues[i][0]==product_ID:
                        DataValues[i]=td                    
                        
            #  Update the displayed table
                window['mytable'].update(values=D_Datavalues)
            #Loop to clean box
                for i in range(5):
                    window[Keylist[i]].update(value='')
                window['Save Edit'].update(disabled=True)
                
                # Update the DataBase

                sql="UPDATE quotation SET product_id='"+td[1]+"', price='"+td[2]+"',Applied_date='"+td[3]+"',supplier='"+td[4]+"' WHERE price_id='"+td[0]+"';"
                cur.execute(sql)  
                # Reset the input boxes
                helper_functions.Reset_data_quotation(window,Keylist)
            else:
                sg.popup('Npt enough data')                 
                
        if event =='Delete row':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:
                if sg.popup_ok_cancel('Can not undo Delete : Contine?')=='OK':
                    
                    # Update the DataBase
                    editRow=values['mytable'][0]                
                    rw=D_Datavalues[editRow]        
                               
                    sql="DELETE FROM quotation WHERE price_id='"+rw[0]+"'"
                    cur.execute(sql)                
                    del D_Datavalues[values['mytable'][0]]    
                                
                    # Update the displayed table
                    window['mytable'].update(values=D_Datavalues)
                    helper_functions.Reset_data_quotation(window,Keylist)
                    
        # Extract to PDF file
        if event=='PDF FILE':
            if values['mytable']==[]:
                sg.popup('No row selected')
            else:            
                editRow=values['mytable'][0]
                sg.popup('Do you want to extract to PDF file?')                   
                Erow=D_Datavalues[editRow] 
                           
                helper_functions.QR_generate(Erow[0],Erow[1],Erow[2],Erow[3],Erow[4])
                helper_functions.PDF_extract_quotation(Erow[0],Erow[1],Erow[2],'qr_code.png',Erow[3],Erow[4])
        if event=='QR scan':
            info=helper_functions.QR_trace()
            for nv in D_Datavalues:
                if nv[0]==info:
                    Erow=nv
                    break
        
            td_update=[Erow[0],Erow[1],Erow[2],Erow[3],Erow[4]]
            
            #Update lên Form Update
            for i in range(5):
                window[Keylist[i]].update(value=td_update[i])            
            window['Save Edit'].update(disabled=False)
            window['PDF FILE'].update(disabled=False) 

    # if conn:
    #     conn.close()
    window.close()
